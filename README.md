# qpid dispatch topology generator

## Generate your configurations

```
python main.py
```

> You can change there the graph or the number of physical machines...

## Deploy it

```
vagrant up
```

> Adjust the number of machine according to the output of the generator

## Access the gui

Browse to `http://192.168.11.2:8000`

Enjoy the topology or generate a new one : 

* Barbell graph (5x5):

![alt text](barbell.png "Barbell")

* Tutte graph (with a bad display)
:
![alt text](tutte.png "Tutte")

# Iteration

```
python generator.py
vagrant provision
vagrant ssh -c "sudo docker ps -aq | xargs sudo docker stop"
vagrant ssh -c "sudo docker ps -aq | xargs sudo docker rm"

