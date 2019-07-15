# splash 动态页面爬取
scrapy处理爬取静态页面，可以说是很好的工具，但是随着技术的发展，现在很多页面都不再是静态页面了，
都是通过AJAX异步加载数据动态生成的，因此需要使用scrapy-splash来动态加载页面之后再爬取数据。

## splash安装
``` 
docker pull scrapinghub/splash

docker run -p 8050:8050 scrapinghub/splash

```

## splash使用
``` 
    splash_url = 'http://192.168.0.23:8050/render.html'
    args = {'url': 'http://quotes.toscrape.com/js', 'timeout': 5, 'image': 0}

    response = requests.get(splash_url, params=args)
    print response.content

    sel = Selector(response)
    sel.css('div.quote span.text::text').extract()
```