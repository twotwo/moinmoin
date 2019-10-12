[![logo](https://raw.githubusercontent.com/twotwo/moinmoin/master/logo.png)](http://moinmo.in/)

# MoinMoin

Moinmoin wiki with Gunicorn docker container

## What is Gunicorn?

Gunicorn (Green Unicorn，绿色独角兽) 是一个WSGI服务器，用来支持Python应用。它是 Ruby 的 Unicorn 服务器的Python实现。Unicorn被设计成轻量级的、易于使用的、并使用许多UNIX特性（UNIX idioms）。Gunicorn不是被设计成面向互联网的 – 它被设计成运行于Nginx之后，缓存慢请求，以及关注其他重要的内容。在 Gunicorn help 能找到 Nginx + Gunicorn 的简单配置步骤。

## How to use this image

### Hosting a simple wiki (still needs a web server in front of it)

    docker run -it --name moinmoin -p 3301:3301 -d --restart=always twotwo/moinmoin

### Complex configuration

    docker-compose up -d

## Development

    docker-compose up --build

### moinmoin source

```
curl -LOS http://static.moinmo.in/files/moin-1.9.10.tar.gz
# macOS
shasum -a 256 moin-1.9.10.tar.gz
```

### code patch

- [MoinHackingOnPage](http://wiki.li3huo.com/MoinHackingOnPage)

`docker cp MoinMoin moinmoin:/usr/local/lib/python2.7/site-packages/`

## Examples



# User Feedback

## Issues

If you have any problems with or questions about this image, please contact me
through a [GitHub issue](https://github.com/twotwo/moinmoin/issues).
