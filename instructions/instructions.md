# European Wireless 2022 Demo instructions

## Demo 1

1. Open a terminal and run the following command:

    ```bash
    ssh -L 8080:192.168.1.2:80 -N testbed.expeca.proj.kth.se
    ```

    This allows you to access the services running on the testbed by opening a browser window and going to [http://localhost:8080](http://localhost:8080).

    Leave this terminal window running in the background.

2. Open another terminal window:
    1. SSH into `galadriel`:
    
        ```bash
        ssh testbed.expeca.proj.kth.se
        ```


    2. `cd` into the `TestbedConfig/ansible` folder:
    
        ```bash
        cd TestbedConfig/ansible
        ```
    
    3. Prepare the Python virtual environment:
    
        ```bash
        source venv/bin/activate
        ```
    
    4. Run the `cleanup_testbed.sh` script: 
    
        ```bash
        ./cleanup_testbed.sh
        ```
        
        This will cleanup whatever is running on the testbed and prepare it for the demo.
    5. Finally, leave this terminal open, as you will need to run the cleanup script again later on.

3. Open a third terminal window:
    1. SSH into `galadriel`:
    
        ```bash
        ssh testbed.expeca.proj.kth.se
        ```

    2. `cd` into the `Ainur` folder: 
    
        ```bash
        cd Ainur
        ```

    3. Make sure you are on the correct `git` branch and you have the latest fixes:
    
        ```bash
        git checkout EWDemo2022 && git pull
        ```

    4. Prepare the environment:

        ```bash
        source venv/bin/activate
        source .env
        ```

    5. Run the desired configuration using the `demo1.py` script.
        1. To run a setup in which client and server run on the same device: 
            
            ```bash
            python demo1.py -l local
            ```

        2. To run a setup in which the server runs on the edge:
        
            ```bash
            python demo1.py -l edge
            ```
        
        3. To run a setup in which the server runs on the cloud:
            
            ```bash
            python demo1.py -l cloud --region eu-west-2
            ```

            The `--region` option can be any of AWS's compute regions, but I recommend sticking with Stockholm (`eu-north-1`, very low latency), London (`eu-west-2`, low-medium latency), US East Coast (`us-east-1`, high latency), and US West coast (`us-west-1`, very high latency).

        4. Any of the above configurations can also be run either over WiFi or Ethernet (default is WiFi). Use the `--phy` flag to specify:

            ```bash
            python demo1.py --phy ethernet -l cloud --region eu-north-1
            ```

        5. Finally, the `demo1.py` script has a help menu:

            ```bash
            python demo1.py --help
            ```

    6. Leave the terminal window open during the demo.

4. Open a browser window and head to [http://localhost:8080](http://localhost:8080) once the system is stable.
    You should see the demo website running there.

5. Finally, when you're done with the demo (or you wish to change the running configuration), run the `cleanup_testbed.sh` script in the second terminal window again.
