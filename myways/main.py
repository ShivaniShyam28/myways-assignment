from get_stats import GetStats

db_string = "postgres://rusejngmnnumvu:83b2d665130d7a045159ff6187d8232470c431cbe8aef1b134d19373b503645d@ec2-54-87-112-29.compute-1.amazonaws.com:5432/d2usd2salsuu27"
get_stats = GetStats(db_string)
function_map = {
    1: get_stats.get_hospital_details,
    2: get_stats.get_empty_beds,
    3: get_stats.get_hospital_items,
    4: get_stats.get_severe_cases_count,
    5: get_stats.get_total_discharged,
}

while True:
    print("Select a information that you want to get:")
    print("1: Hospital Details")
    print("2: Number of Empty beds in hospitals")
    print("3: Hospital Item Details")
    print("4: Number of Sever cases count")
    print("5: Total Discharged")
    try:
        number = int(input("Enter a number: "))
        function_map[number]()
    except KeyboardInterrupt:
        exit()
    except:
        print("Invalid number")
    
    
