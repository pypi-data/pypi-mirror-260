# damip

Python SDK for Digitopia Advanced Mechanical Intelligence Platform(DAMIP).

### Installation

We use PyPI to distribute our software.

```sh
$ pip install damip
```


### Usage

```python
>>> from damip import oldtimes
>>> mybot = oldtimes.robot()
>>> mybot.hello()
'hello, I am an oldtimes robot, My name is Oldtimes.'
>>> mybot.right_arm_shake(1)
:) Send:  {"T":50,"id":2,"pos":300,"spd":500,"acc":30} 44
:) Set right arm postion:  300
:) Send:  {"T":50,"id":2,"pos":700,"spd":500,"acc":30} 44
:) Set right arm postion:  700
:) Send:  {"T":50,"id":2,"pos":500,"spd":500,"acc":30} 44
```
