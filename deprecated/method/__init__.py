def schedule_details(flights: list, sep: dict, perm: list)->tuple:
    tot_delay = 0
    details = []
    
    last_take_off_time = -24*60
    last_take_off_type = 'L'

    for i in perm:
        flight = flights[i]
        earliest_take_off_time = flight['EOBT'] + flight['SLIP']
        take_off = max(earliest_take_off_time, 
                       last_take_off_time + sep[last_take_off_type][flight['type']])
        slip_start = take_off - flight['SLIP']

        last_take_off_time = take_off
        last_take_off_type = flight['type']

        details.append({'slip start': slip_start, 'take off': take_off})
        tot_delay += slip_start - flight['EOBT']
    
    return details, tot_delay
