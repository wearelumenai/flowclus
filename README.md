# Build an online clustering and visualization app in less than 100 lines of code 
> Tutorial

# Introduction
In this tutorial, we will see how to integrate two libraries :
[distclus4py](https://github.com/wearelumenai/distclus4py)
and
[bubbles4py](https://github.com/wearelumenai/bubbles4py)
in order to modelize a data flow online.

# requirements
This demo needs Python 3.7 to run. It is recommended to use a virtualenv.

# Build ans install the components
First you need to properly install the two libraries :
 - [distclus4py](https://github.com/wearelumenai/distclus4py)
 - [bubbles4py](https://github.com/wearelumenai/bubbles4py)

**_Note_** : follow carefully the instruction given in the README of these
libraries.

Then download this demo and continue as follows to install the libraries :

```
$ cd flowclust
$ python3.7 -m venv ./venv
$ . ./venv/bin/activate
(venv) $ pip install Cython numpy scipy # because POT is flawed
(venv) $ python setup.py install
(venv) $ pip install <path/to/disclus4py>
(venv) $ pip install <path/to/bubbles4py>
```

# Run the demo

First run a simulation server that deliver a dataflow :

```
$ python -m flowsim &
```

Now you should be able to get data points :

```
$ curl -XGET 'http://localhost:8080/points?start=2019-06-26T15:39&stop=2019-06-26T15:40'
```

http://localhost:8081/bubbles?result_id=batch_tutorial