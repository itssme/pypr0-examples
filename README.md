# Examples for pip package pypr0
https://github.com/itssme/pypr0

## Example 1
Crawls back x days of /top and then shows some statistics about them using the pip ```statistics``` package.

Then they are inserted into the database using the db manager and some select statements are demonstrated.

## Example 2
Crawls all posts with the tag ```schmuserkadser``` and then starts downloading them until the user presses <kbd>ctrl</kbd>+<kbd>c</kbd> or all posts are downloaded.

# Code Snippets

## Api
```python
from pr0gramm import *
api = Api()
```
Without login some request will fail (for example: getting comments, the inbox etc.)

### With login
```python
api = Api("username", "password")
```

## Get newest post
```python
api.get_newest_image()
```

### As Post() object
This is done because now the json string returned by ```Api.get_newest_image()``` is parsed.
```python
Post(api.get_newest_image())
```

And we can access all its attributes
```python
Post(api.get_newest_image()).keys()
>> dict_keys(['up', 'gift', 'flags', 'width', 'thumb', 'fullsize', 'image', 'audio', 'source', 'promoted', 'down', 'mark', 'height', 'created', 'user', 'userId', 'id'])
```

### Getting id of newest post from Post() object
```python
Post(api.get_newest_image()).keys()["id"]
>> 1234566789
```

### Getting points of newest post in /top using Post() object
```python
post = Post(api.get_newest_image(promoted=1))
print(post["up"]-post["down"])
>> 12345
```
Beware: This will use a flag of ```1``` which means that only publicly available posts tagged swf (not nsfp) will be used.
