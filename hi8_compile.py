import sys
import time
import hi8_fetch

# Parse command line
day = int(sys.argv[1])
scale = int(sys.argv[2])


# Send off to function
# python ./hi8-fetch.py "{yr}-{mo}-{dy} {hr}:{tenmin}0:00" {scale} raw/{yr}-{mo}-{dy}T{hr}{tenmin}000.png' 
# ::: yr 2016 ::: mo 01 ::: dy $df ::: hr {14..23} ::: tenmin {0..5} ::: scale $scale

# Iterate over the hours
for hr in range(0,24):
    # Itterate over the tenmin (what is this? idk)
    tenmin = 0
    while tenmin < 5:
        # Create date stamp
        str_day = "2016-01-"+str(day)+"T"+str(hr)+":"+str(tenmin)+"0:00"
        str_out = "2016-01-"+str(day)+"T"+str(hr)+str(tenmin)+"000-z"+str(scale)+".png"

        try:
            # Call function
            hi8_fetch.fetch_day(str_day, scale, str_out)
        except Exception as e:
            # If error, loop this fetch
            tenmin-=1
            print("Error = Relooping")
            print(e)

        # Debug
        print("Exported = "+str_out)
        # Move loop forward
        tenmin+=1
    
