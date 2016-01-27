import sys
import time
import hi8_fetch
import threading

# Parse command line
day = int(sys.argv[1])
scale = int(sys.argv[2])


# Send off to function
# python ./hi8-fetch.py "{yr}-{mo}-{dy} {hr}:{tenmin}0:00" {scale} raw/{yr}-{mo}-{dy}T{hr}{tenmin}000.png' 
# ::: yr 2016 ::: mo 01 ::: dy $df ::: hr {14..23} ::: tenmin {0..5} ::: scale $scale

# Iterate over the hours
hr = 0
while hr < 24:
    # Create datestamp
    str_day_1 = "2016-01-"+str(day)+"T"+str(hr)+":"+str(1)+"0:00"
    str_day_2 = "2016-01-"+str(day)+"T"+str(hr)+":"+str(2)+"0:00"
    str_day_3 = "2016-01-"+str(day)+"T"+str(hr)+":"+str(3)+"0:00"
    str_day_4 = "2016-01-"+str(day)+"T"+str(hr)+":"+str(4)+"0:00"
    str_day_5 = "2016-01-"+str(day)+"T"+str(hr)+":"+str(5)+"0:00"
    # Output strings
    str_out_1 = "2016-01-"+str(day)+"T"+str(hr)+str(1)+"000-z"+str(scale)+".png"
    str_out_2 = "2016-01-"+str(day)+"T"+str(hr)+str(2)+"000-z"+str(scale)+".png"
    str_out_3 = "2016-01-"+str(day)+"T"+str(hr)+str(3)+"000-z"+str(scale)+".png"
    str_out_4 = "2016-01-"+str(day)+"T"+str(hr)+str(4)+"000-z"+str(scale)+".png"
    str_out_5 = "2016-01-"+str(day)+"T"+str(hr)+str(5)+"000-z"+str(scale)+".png"

    try:
        # Call function
        t1 = threading.Thread(target=hi8_fetch.fetch_day, args=(str_day_1, scale, str_out_1))
        t1.daemon = True
        t2 = threading.Thread(target=hi8_fetch.fetch_day, args=(str_day_2, scale, str_out_2))
        t2.daemon = True
        t3 = threading.Thread(target=hi8_fetch.fetch_day, args=(str_day_3, scale, str_out_3))
        t3.daemon = True
        t4 = threading.Thread(target=hi8_fetch.fetch_day, args=(str_day_4, scale, str_out_4))
        t4.daemon = True
        t5 = threading.Thread(target=hi8_fetch.fetch_day, args=(str_day_5, scale, str_out_5))
        t5.daemon = True

        # Start threads
        t1.start();
        t2.start();
        t3.start();
        t4.start();
        t5.start();

        # Wait for them to join back up
        while True:
            t1.join(10);
            t2.join(10);
            t3.join(10);
            t4.join(10);
            t5.join(10);
            # Check to see if all threads have exited
            if not t1.isAlive() and not t2.isAlive() and not t3.isAlive() and not t4.isAlive() and not t5.isAlive():
                break
        

        # Stop threads
        t1._stop();
        t2._stop();
        t3._stop();
        t4._stop();
        t5._stop();

        #hi8_fetch.fetch_day(str_day_1, scale, str_out_1)
    
    except Exception as e:
        # If error, loop this fetch
        hr-=1
        print("Error = Relooping")
        print(e)

    # Debug
    print("Exported = 2016-01-"+str(day)+"T"+str(hr)+":000:00")
    # Move loop forward
    hr+=1
    
