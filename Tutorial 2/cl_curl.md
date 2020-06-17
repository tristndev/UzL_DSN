# `clbin` (pastebin for the commandline)

## Upload

```
echo hello world | curl -F 'clbin=<-' https://clbin.com
```

**returns**: the clbin.com url

## Download

### To console

```
curl <clbin.com url>
```

### To file

```
curl https://clbin.com/2HUF6 > file.txt
```





