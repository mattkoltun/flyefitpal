#!/usr/bin/env python
import sys, getopt, traceback
from datetime import datetime, timedelta
from flyefitpal import WorkoutSession, FlyefitPal, GymSiteNotFound, WrongTimeSlotException, \
        FullyBookedException, AlreadyBookedException, NotYetAvailableException, \
        DailyLimitReachedException


help_message = \
        "+------------------------+\n" + \
        "| Flyefit Booking Script |\n" + \
        "+------------------------+\n" + \
        "\nSynopsis:\n" + \
        "\tmain.py -e <email> -p <password> -s <site> -t <time_slot>\n\n" + \
        "\te.g.\tmain.py -e me@exmaple.com -p supersecret123 " + \
        "\-s 'Liffey Valley' -t '13:30 - 14:45'\n\n" + \
        "\t-e, --email\t\t: Login email\n" + \
        "\t-p, --password\t\t: Login password\n" + \
        "\t-s, --site\t\t: Gym location, must be exactly the same as on the Website\n" + \
        "\t\t\t\t\te.g. 'Liffey Valey', 'Cork City', 'CHQ', 'Swords'\n" + \
        "\t-t, --time\t\t: Session time (24hrs format), must be exactly the same as on the Website\n" + \
        "\t\t\t\t\te.g. '05:30 - 06:45', '15:00 - 16:15', '10:15 - 11:30'\n" + \
        "\t-h, --help\t\t: Print this message\n\n"

def formatted_tomorrow_date():
    tom = datetime.now() + timedelta(days=1)
    return "{:d}-{:02d}-{:02d}".format(tom.year, tom.month, tom.day)

def main(email, password, site, time):
    try:
        pal = FlyefitPal(email, password)
        session = WorkoutSession(site, time, formatted_tomorrow_date())
        pal.book_workout(session)
    except GymSiteNotFound as e:
        print(e)
        sys.exit(1)
    except FullyBookedException as e:
        print(e)
        sys.exit(1)
    except AlreadyBookedException as e:
        print(e)
        sys.exit(1)
    except NotYetAvailableException as e:
        print(e)
        sys.exit(1)
    except DailyLimitReachedException as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print("---------------\n", e, "\n---------------")
        print(traceback.format_exc())
        sys.exit(1)
    else:
        print("Workout session booked successfully.")
        sys.exit()

if __name__ == "__main__":
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "e:p:s:t:h", ["email=", "password=", "site=", "time=", "help"])
    except getopt.GetoptError:
        print("run --help")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_message)
            sys.exit()
        elif opt in ("-e", "--email"):
            email = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-s", "--site"):
            site = arg
        elif opt in ("-t", "--time"):
            time = arg
    if not email or not password or not site or not time:
        print("Missing required arguments. Run help for more information:\n\tmain.py --help")
        sys.exit(1)
    main(email, password, site, time)
