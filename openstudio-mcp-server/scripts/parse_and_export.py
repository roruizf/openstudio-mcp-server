#!/usr/bin/env python3
"""
Parse OpenStudio `.osm` text files (IDF-style) to extract:
- Thermal zones and aggregated floor area/volume per zone (from `OS:Space` assignments)
- Lighting objects and compute lighting W/m2 per space using Lights Definitions

Writes:
- `outputs/vgp_montijo_thermal_zones.json`
- `outputs/vgp_montijo_thermal_zones.csv`
- `outputs/r2f_top_lighting_w_per_m2.csv`

This is a lightweight parser that relies on the IDF-like layout used in these OSMs.
It does not use OpenStudio Python bindings so it is portable in CI / developer shells.
"""
import csv
import json
import os
import re
from collections import defaultdict


def read_objects(osm_path):
    """Yield (type_name, values_list) for each OS:* object in the file."""
    objs = []
    with open(osm_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        if line.startswith('OS:'):
            # object header like: OS:Space,
            type_name = line.split(',')[0].strip()
            i += 1
            values = []
            # collect fields until a line ending with ';'
            while i < n:
                raw = lines[i]
                i += 1
                # remove comment starting with '!' if present
                if '!' in raw:
                    raw = raw.split('!')[0]
                # remove trailing commas/newlines
                raw = raw.strip()
                if raw.endswith(','):
                    raw = raw[:-1].strip()
                if raw.endswith(';'):
                    raw = raw[:-1].strip()
                    if raw == '':
                        values.append('')
                    else:
                        values.append(raw)
                    break
                if raw == '':
                    values.append('')
                else:
                    values.append(raw)
            objs.append((type_name, values))
        else:
            i += 1
    return objs


def parse_montijo(osm_path):
    objs = read_objects(osm_path)
    # maps
    zones = {}             # handle -> name
    thermostats = {}      # handle -> name (if found)
    spaces = {}           # handle -> dict(name, floor_area, volume, zone_handle)

    for typ, vals in objs:
        if typ == 'OS:ThermostatSetpoint:DualSetpoint' or typ.startswith('OS:Thermostat'):
            # Handle, Name, ...
            if len(vals) >= 2:
                handle = vals[0]
                name = vals[1]
                thermostats[handle] = name
        elif typ == 'OS:ThermalZone':
            # Handle, Name, ... thermostat is often near the end; we'll capture by handle->name
            if len(vals) >= 2:
                handle = vals[0]
                name = vals[1]
                # attempt to find thermostat handle in the values (UUID-like {..})
                thermo = None
                for v in reversed(vals):
                    if v.startswith('{') and v.endswith('}'):
                        # skip first few that are ports etc — but take the first uuid-like that also appears in thermostats
                        if v in thermostats:
                            thermo = thermostats[v]
                            break
                        elif thermo is None:
                            thermo = v
                zones[handle] = {'name': name, 'thermostat': thermo}
        elif typ == 'OS:Space':
            # fields: handle, name, ..., thermal zone handle (index 10), ..., volume(index -3?), floor area(last)
            handle = vals[0] if len(vals) >= 1 else None
            name = vals[1] if len(vals) >= 2 else ''
            # thermal zone handle commonly at index 10 (0-based)
            zone_handle = vals[10] if len(vals) > 10 else ''
            # floor area usually last field
            floor_area = 0.0
            volume = 0.0
            try:
                if len(vals) >= 17:
                    fa = vals[16]
                    floor_area = float(fa) if fa not in ('', None) else 0.0
                else:
                    # fallback: last field
                    fa = vals[-1]
                    floor_area = float(fa) if fa not in ('', None) else 0.0
            except Exception:
                floor_area = 0.0
            try:
                # volume is often the field before ceiling height / floor area
                vol_field = vals[-3] if len(vals) >= 3 else ''
                volume = float(vol_field) if vol_field not in ('', None) else 0.0
            except Exception:
                volume = 0.0
            spaces[handle] = {'name': name, 'floor_area': floor_area, 'volume': volume, 'zone_handle': zone_handle}

    # aggregate spaces into zones
    zone_agg = {}
    for zhandle, zinfo in zones.items():
        zone_agg[zhandle] = {
            'name': zinfo['name'],
            'thermostat': zinfo.get('thermostat'),
            'floor_area_m2': 0.0,
            'volume_m3': 0.0,
            'spaces': []
        }

    # spaces whose zone is not listed: add them under None
    for sh, sinfo in spaces.items():
        zh = sinfo['zone_handle']
        if zh in zone_agg:
            zone_agg[zh]['floor_area_m2'] += sinfo['floor_area']
            zone_agg[zh]['volume_m3'] += sinfo['volume']
            zone_agg[zh]['spaces'].append({'space_handle': sh, 'space_name': sinfo['name'], 'floor_area_m2': sinfo['floor_area'], 'volume_m3': sinfo['volume']})
        else:
            # create an 'unassigned' zone entry if necessary
            no_key = zh or 'UNASSIGNED'
            if no_key not in zone_agg:
                zone_agg[no_key] = {'name': no_key, 'thermostat': None, 'floor_area_m2': 0.0, 'volume_m3': 0.0, 'spaces': []}
            zone_agg[no_key]['floor_area_m2'] += sinfo['floor_area']
            zone_agg[no_key]['volume_m3'] += sinfo['volume']
            zone_agg[no_key]['spaces'].append({'space_handle': sh, 'space_name': sinfo['name'], 'floor_area_m2': sinfo['floor_area'], 'volume_m3': sinfo['volume']})

    # prepare neat list for json/csv
    rows = []
    for zh, data in zone_agg.items():
        rows.append({
            'zone_handle': zh,
            'zone_name': data['name'],
            'thermostat': data['thermostat'],
            'floor_area_m2': round(data['floor_area_m2'], 3),
            'volume_m3': round(data['volume_m3'], 3),
            'n_spaces': len(data['spaces'])
        })

    return rows


def parse_r2f_lighting(osm_path):
    objs = read_objects(osm_path)
    # maps
    lights_defs = {}   # handle -> {method, lighting_level, watts_per_area, watts_per_person}
    spaces = {}        # handle -> {name, floor_area}
    lights = []        # list of lights objects

    for typ, vals in objs:
        if typ == 'OS:Lights:Definition':
            handle = vals[0] if len(vals) >= 1 else None
            name = vals[1] if len(vals) >= 2 else ''
            method = vals[2] if len(vals) >= 3 else ''
            lighting_level = float(vals[3]) if len(vals) >= 4 and vals[3] not in ('', None) else 0.0
            watts_per_area = float(vals[4]) if len(vals) >= 5 and vals[4] not in ('', None) else 0.0
            watts_per_person = float(vals[5]) if len(vals) >= 6 and vals[5] not in ('', None) else 0.0
            lights_defs[handle] = {'name': name, 'method': method, 'lighting_level_w': lighting_level, 'watts_per_area': watts_per_area, 'watts_per_person': watts_per_person}
        elif typ == 'OS:Space':
            handle = vals[0] if len(vals) >= 1 else None
            name = vals[1] if len(vals) >= 2 else ''
            # floor area usually last field
            floor_area = 0.0
            try:
                if len(vals) >= 17:
                    floor_area = float(vals[16]) if vals[16] != '' else 0.0
                else:
                    floor_area = float(vals[-1]) if vals[-1] != '' else 0.0
            except Exception:
                floor_area = 0.0
            spaces[handle] = {'name': name, 'floor_area': floor_area}
        elif typ == 'OS:Lights':
            # handle, name, lights definition name (handle), space or spaceType (handle), schedule, fraction replaceable, multiplier, enduse
            handle = vals[0] if len(vals) >= 1 else None
            name = vals[1] if len(vals) >= 2 else ''
            def_handle = vals[2] if len(vals) >= 3 else ''
            space_handle = vals[3] if len(vals) >= 4 else ''
            multiplier = float(vals[6]) if len(vals) >= 7 and vals[6] not in ('', None) else 1.0
            lights.append({'handle': handle, 'name': name, 'def_handle': def_handle, 'space_handle': space_handle, 'multiplier': multiplier})

    # compute W/m2 per space by summing contributions
    space_power_w = defaultdict(float)
    for l in lights:
        d = lights_defs.get(l['def_handle'], None)
        space = spaces.get(l['space_handle'], None)
        if not d or not space:
            continue
        method = d.get('method', '')
        if method == 'Watts/Area' and d.get('watts_per_area', 0.0) > 0.0:
            wpm2 = d['watts_per_area'] * l['multiplier']
            space_power_w[l['space_handle']] += wpm2 * space['floor_area']
        elif method == 'LightingLevel' and d.get('lighting_level_w', 0.0) > 0.0:
            # lighting level is absolute W for the object
            total_w = d['lighting_level_w'] * l['multiplier']
            space_power_w[l['space_handle']] += total_w
        elif d.get('watts_per_area', 0.0) > 0.0:
            # fallback
            wpm2 = d['watts_per_area'] * l['multiplier']
            space_power_w[l['space_handle']] += wpm2 * space['floor_area']
        else:
            # unknown -> skip
            continue

    # compute W/m2
    results = []
    for sh, p_total_w in space_power_w.items():
        sp = spaces.get(sh)
        area = sp['floor_area'] if sp else 0.0
        w_per_m2 = p_total_w / area if area > 0 else 0.0
        results.append({'space_handle': sh, 'space_name': sp['name'] if sp else '', 'floor_area_m2': area, 'lighting_w_total': round(p_total_w,3), 'lighting_w_per_m2': round(w_per_m2,3)})

    # sort descending by w_per_m2
    results.sort(key=lambda x: x['lighting_w_per_m2'], reverse=True)
    return results


def ensure_out_dir():
    os.makedirs('outputs', exist_ok=True)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_csv(path, rows, headers):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main():
    ensure_out_dir()
    montijo_path = 'sample_files/models/VGP-Montijo-009.osm'
    r2f_path = 'sample_files/models/R2F-Office-Hub-006.osm'

    print('Parsing Montijo OSM...')
    montijo_rows = parse_montijo(montijo_path)
    write_json('outputs/vgp_montijo_thermal_zones.json', montijo_rows)
    # write CSV with selected fields
    csv_rows = [{'zone_handle': r['zone_handle'], 'zone_name': r['zone_name'], 'thermostat': r['thermostat'], 'floor_area_m2': r['floor_area_m2'], 'volume_m3': r['volume_m3'], 'n_spaces': r['n_spaces']} for r in montijo_rows]
    write_csv('outputs/vgp_montijo_thermal_zones.csv', csv_rows, ['zone_handle','zone_name','thermostat','floor_area_m2','volume_m3','n_spaces'])
    print('Wrote outputs/vgp_montijo_thermal_zones.json and .csv')

    print('Parsing R2F lighting...')
    r2f_results = parse_r2f_lighting(r2f_path)
    top10 = r2f_results[:10]
    write_csv('outputs/r2f_top_lighting_w_per_m2.csv', top10, ['space_handle','space_name','floor_area_m2','lighting_w_total','lighting_w_per_m2'])
    print('Wrote outputs/r2f_top_lighting_w_per_m2.csv')


if __name__ == '__main__':
    main()
