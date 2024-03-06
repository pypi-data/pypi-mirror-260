# The Brookhaven Group, LLC (TBG) Utilities
*Date and string utilities*

These are utilities commonoly used at The Brookhaven Group, LLC


### Installation

[PyPI Page](https://pypi.org/search/?q=tbgutils)

```shell
$ pip install tbgutils 
```

or 

[GitHub](https://github.com/TheBrookhavenGroup/tbgutils)

```shell
$ pip install  git+https://github.com/TheBrookhavenGroup/tbgutils.git
```

### Examples

#### Print the beginning of the next day in local time.
```
>>> from tbgutils.dt import to_date, day_start_next_day
>>> d = to_date('20230320')
>>> print(day_start_next_day(d))
"2023-03-21 04:00:00+00:00
```

#### Is holiday observed?
```python
>>> from src.tbgutils.dt import to_date, is_holiday_observed
>>> d = to_date('20230704')
>>> is_holiday_observed(d)
True
```

#### Is it a weekend?
```python
>>> from src.tbgutils.dt import is_week_end
>>> d = to_date('20230704')
>>> is_week_end(d)
False
>>> d = to_date('20230319')
>>> is_week_end(d)
True
```

# THE END
