SCRAPER_SETTINGS = {
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 60.0,
    'AUTOTHROTTLE_MAX_DELAY': 300.0,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
    'AUTOTHROTTLE_DEBUG': True,
    'DOWNLOAD_DELAY': 30.0,
    'CONCURRENT_REQUESTS_PER_IP': 1,
    'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
}


def get_feed_settings(class_name):
    return {
        'FEED_FORMAT': 'json',
        'FEED_URI': f'/scrapers-data/json/{class_name}.json',
        'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
    }