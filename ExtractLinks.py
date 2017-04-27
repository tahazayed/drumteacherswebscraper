#http://www.drumteachers.co.uk/find-a-teacher/index.php?sort=ASC&limit=50&page=1&order=&browse=all#rs
import scrapy
from time import sleep
 
pageid = 1

class BlogSpider(scrapy.Spider):
    name = 'drumteachers'

    start_urls = ['http://www.drumteachers.co.uk/find-a-teacher/index.php?sort=ASC&limit=50&page=1&order=&browse=all#rs']
    
    
    def parse(self, response):
        with open("links.txt", 'a') as f:
            for title in response.css("div[class='teacherTitleText'] > *"):
                print(title.css('a ::attr(href)'))
                f.write(title.css('a ::attr(href)').extract_first().replace('/find-a-teacher/profile/?tuid=','')+"\n")
            f.flush()
            f.close()
            
           

        global pageid
        print("pageid:{}".format(pageid))
        if pageid < 12:
            pageid = pageid+1    
            next_page = 'http://www.drumteachers.co.uk/find-a-teacher/index.php?sort=ASC&limit=50&page={}&order=&browse=all#rs'.format(str(pageid))
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse, \
				headers={'Referer':'http://www.drumteachers.co.uk/find-a-teacher/index.php?sort=ASC&limit=50&page={}&order=&browse=all#rs'.format(str(pageid-1))})