import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    # 获取项目设置
    settings = get_project_settings()

    # 设置 MaoYan 爬虫专属 FEEDS 配置
    settings['FEEDS'] = {
        r'D:/Code/Database/movie.json': {
            'format': 'json',
            'overwrite': True,
            'item_classes': ['ScrapyProject.items.MovieItem']
        },
        r'D:/Code/Database/actor.json': {
            'format': 'json',
            'overwrite': True,
            'item_classes': ['ScrapyProject.items.ActorItem']
        },
        r'D:/Code/Database/movieActor.json': {
            'format': 'json',
            'overwrite': True,
            'item_classes': ['ScrapyProject.items.MovieActorItem']
        }
    }

    # 创建爬虫进程
    process = CrawlerProcess(settings)

    # 添加要启动的爬虫
    process.crawl('MaoYan')

    # 启动爬虫
    process.start()

if __name__ == "__main__":
    main()
