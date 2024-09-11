from sqlalchemy import Column, Integer, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'Product'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(Text, nullable=False)
    shipped_from = Column(Text, nullable=False)
    product_category = Column(Text, nullable=False)
    tiktok_product_link = Column(Text, nullable=False)
    product_price = Column(Text, nullable=False)
    lowest_price_30_days = Column(Text, nullable=False)
    product_earliest_date_recorded = Column(Text, nullable=False)
    from_shop_name = Column(Text, nullable=False)
    image_links = Column(Text, nullable=False)
    revenue_entity_id = Column(Integer, nullable=False)
    video_revenue_entity_id = Column(Integer, nullable=False)
    live_revenue_entity_id = Column(Integer, nullable=False)
    avg_unit_price_entity_id = Column(Integer, nullable=False)
    item_sold_entity_id = Column(Integer, nullable=False)
    mall_revenue_entity_id = Column(Integer, nullable=False)

class Creator(Base):
    __tablename__ = 'Creator'

    creator_id = Column(Integer, primary_key=True, autoincrement=True)
    creator_username = Column(Text, nullable=False)
    no_of_followers = Column(Text, nullable=False)
    debut_time = Column(Text, nullable=False)
    last_30_days_products = Column(Integer, nullable=False)
    creator_bio = Column(Text, nullable=False)
    tiktok_link = Column(Text)
    instagram_link = Column(Text)
    contact_email_address = Column(Text)
    creator_earliest_date_recorded = Column(Text, nullable=False)
    revenue_entity_id = Column(Integer, nullable=False)
    live_revenue_entity_id = Column(Integer, nullable=False)
    video_revenue_entity_id = Column(Integer, nullable=False)
    avg_unit_price_entity_id = Column(Integer, nullable=False)
    traffic_live_views_yesterday = Column(Text, nullable=False)
    traffic_live_views_per_day_last_7_days = Column(Text, nullable=False)
    traffic_live_views_per_day_last_30_days = Column(Text, nullable=False)
    traffic_live_views_per_day_last_90_days = Column(Text, nullable=False)
    traffic_live_views_per_day_last_180_days = Column(Text, nullable=False)
    traffic_live_views_last_7_days = Column(Text, nullable=False)
    traffic_live_views_last_30_days = Column(Text, nullable=False)
    traffic_live_views_last_90_days = Column(Text, nullable=False)
    traffic_live_views_last_180_days = Column(Text, nullable=False)
    video_views_yesterday = Column(Text, nullable=False)
    video_views_per_day_last_7_days = Column(Text, nullable=False)
    video_views_per_day_last_30_days = Column(Text, nullable=False)
    video_views_per_day_last_90_days = Column(Text, nullable=False)
    video_views_per_day_last_180_days = Column(Text, nullable=False)
    video_views_last_7_days = Column(Text, nullable=False)
    video_views_last_30_days = Column(Text, nullable=False)
    video_views_last_90_days = Column(Text, nullable=False)
    video_views_last_180_days = Column(Text, nullable=False)
    new_followers_yesterday = Column(Text, nullable=False)
    new_followers_per_day_last_7_days = Column(Text, nullable=False)
    new_followers_per_day_last_30_days = Column(Text, nullable=False)
    new_followers_per_day_last_90_days = Column(Text, nullable=False)
    new_followers_per_day_last_180_days = Column(Text, nullable=False)
    new_followers_last_7_days = Column(Text, nullable=False)
    new_followers_last_30_days = Column(Text, nullable=False)
    new_followers_last_90_days = Column(Text, nullable=False)
    new_followers_last_180_days = Column(Text, nullable=False)

class Video(Base):
    __tablename__ = 'Video'

    video_id = Column(Integer, primary_key=True, autoincrement=True)
    video_link = Column(Text, nullable=False)
    video_tags = Column(Text)
    video_music_info = Column(Text)
    revenue_entity_id = Column(Integer, nullable=False)
    video_revenue_entity_id = Column(Integer, nullable=False)
    item_sold_entity_id = Column(Integer, nullable=False)
    video_publish_date = Column(Text, nullable=False)
    video_duration = Column(Text, nullable=False)
    video_advertising_information = Column(Text)
    video_earliest_date_recorded = Column(Text, nullable=False)

    # from_creator = Column(Text, nullable=False)
    # on_product = Column(Text, nullable=False)


    # Video views data
    video_views_yesterday = Column(Text, nullable=False)
    video_views_per_day_last_7_days = Column(Text, nullable=False)
    video_views_per_day_last_30_days = Column(Text, nullable=False)
    video_views_per_day_last_90_days = Column(Text, nullable=False)
    video_views_per_day_last_180_days = Column(Text, nullable=False)
    video_views_last_7_days = Column(Text, nullable=False)
    video_views_last_30_days = Column(Text, nullable=False)
    video_views_last_90_days = Column(Text, nullable=False)
    video_views_last_180_days = Column(Text, nullable=False)

    # Video new followers data
    video_new_followers_yesterday = Column(Text, nullable=False)
    video_new_followers_per_day_last_7_days = Column(Text, nullable=False)
    video_new_followers_per_day_last_30_days = Column(Text, nullable=False)
    video_new_followers_per_day_last_90_days = Column(Text, nullable=False)
    video_new_followers_per_day_last_180_days = Column(Text, nullable=False)
    video_new_followers_last_7_days = Column(Text, nullable=False)
    video_new_followers_last_30_days = Column(Text, nullable=False)
    video_new_followers_last_90_days = Column(Text, nullable=False)
    video_new_followers_last_180_days = Column(Text, nullable=False)

    # Video ad view ratio data
    video_ad_view_ratio_yesterday = Column(Text, nullable=False)
    video_ad_view_ratio_last_7_days = Column(Text, nullable=False)
    video_ad_view_ratio_last_30_days = Column(Text, nullable=False)
    video_ad_view_ratio_last_90_days = Column(Text, nullable=False)
    video_ad_view_ratio_last_180_days = Column(Text, nullable=False)

    # Video ad revenue ratio data
    video_ad_revenue_ratio_yesterday = Column(Text, nullable=False)
    video_ad_revenue_ratio_last_7_days = Column(Text, nullable=False)
    video_ad_revenue_ratio_last_30_days = Column(Text, nullable=False)
    video_ad_revenue_ratio_last_90_days = Column(Text, nullable=False)
    video_ad_revenue_ratio_last_180_days = Column(Text, nullable=False)

    # Video ad spend data
    video_ad_spend_yesterday = Column(Text, nullable=False)
    video_ad_spend_last_7_days = Column(Text, nullable=False)
    video_ad_spend_last_30_days = Column(Text, nullable=False)
    video_ad_spend_last_90_days = Column(Text, nullable=False)
    video_ad_spend_last_180_days = Column(Text, nullable=False)

    # Video ad ROAS (Return on Ad Spend) data
    video_ad_roas_yesterday = Column(Text, nullable=False)
    video_ad_roas_last_7_days = Column(Text, nullable=False)
    video_ad_roas_last_30_days = Column(Text, nullable=False)
    video_ad_roas_last_90_days = Column(Text, nullable=False)
    video_ad_roas_last_180_days = Column(Text, nullable=False)

class Live_Stream(Base):
    __tablename__ = 'Live_Stream'

    live_stream_id = Column(Integer, primary_key=True, autoincrement=True)
    live_stream_name = Column(Text)
    live_stream_product_count = Column(Text, nullable=False)
    live_revenue_entity_id = Column(Integer, nullable=False)
    avg_unit_price_entity_id = Column(Integer, nullable=False)
    item_sold_entity_id = Column(Integer, nullable=False)
    live_stream_top_3_category = Column(Text, nullable=False)
    live_stream_time = Column(Text, nullable=False)
    live_stream_duration = Column(Text, nullable=False)
    live_stream_creator = Column(Text, nullable=False)
    live_stream_online_viewers = Column(Text, nullable=False)
    live_stream_online_viewers_per_minute = Column(Text, nullable=False)
    live_stream_views = Column(Text, nullable=False)
    live_stream_views_per_minute = Column(Text, nullable=False)
    live_stream_item_sold = Column(Text, nullable=False)
    live_stream_item_sold_per_minute = Column(Text, nullable=False)

class Shop(Base):
    __tablename__ = 'Shop'

    shop_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(Text, nullable=False)
    shop_type = Column(Text, nullable=False)
    shop_earliest_date_recorded = Column(Text, nullable=False)
    revenue_entity_id = Column(Integer, nullable=False)
    avg_unit_price_entity_id = Column(Integer, nullable=False)
    item_sold_entity_id = Column(Integer, nullable=False)
    mall_revenue_entity_id = Column(Integer, nullable=False)

    # Shop SOA revenue data
    shop_soa_revenue_yesterday = Column(Text, nullable=False)
    shop_soa_revenue_per_day_last_7_days = Column(Text, nullable=False)
    shop_soa_revenue_per_day_last_30_days = Column(Text, nullable=False)
    shop_soa_revenue_per_day_last_90_days = Column(Text, nullable=False)
    shop_soa_revenue_per_day_last_180_days = Column(Text, nullable=False)
    shop_soa_revenue_last_7_days = Column(Text, nullable=False)
    shop_soa_revenue_last_30_days = Column(Text, nullable=False)
    shop_soa_revenue_last_90_days = Column(Text, nullable=False)
    shop_soa_revenue_last_180_days = Column(Text, nullable=False)

    # Shop affiliate revenue data
    shop_affiliate_revenue_yesterday = Column(Text, nullable=False)
    shop_affiliate_revenue_per_day_last_7_days = Column(Text, nullable=False)
    shop_affiliate_revenue_per_day_last_30_days = Column(Text, nullable=False)
    shop_affiliate_revenue_per_day_last_90_days = Column(Text, nullable=False)
    shop_affiliate_revenue_per_day_last_180_days = Column(Text, nullable=False)
    shop_affiliate_revenue_last_7_days = Column(Text, nullable=False)
    shop_affiliate_revenue_last_30_days = Column(Text, nullable=False)
    shop_affiliate_revenue_last_90_days = Column(Text, nullable=False)
    shop_affiliate_revenue_last_180_days = Column(Text, nullable=False)

    # Shop SOA revenue share data
    shop_soa_revenue_share_yesterday = Column(Text, nullable=False)
    shop_soa_revenue_share_last_7_days = Column(Text, nullable=False)
    shop_soa_revenue_share_last_30_days = Column(Text, nullable=False)
    shop_soa_revenue_share_last_90_days = Column(Text, nullable=False)
    shop_soa_revenue_share_last_180_days = Column(Text, nullable=False)

    # Shop affiliate revenue share data
    shop_aff_revenue_share_yesterday = Column(Text, nullable=False)
    shop_aff_revenue_share_last_7_days = Column(Text, nullable=False)
    shop_aff_revenue_share_last_30_days = Column(Text, nullable=False)
    shop_aff_revenue_share_last_90_days = Column(Text, nullable=False)
    shop_aff_revenue_share_last_180_days = Column(Text, nullable=False)

    # Shop mall revenue share data
    shop_mall_revenue_share_yesterday = Column(Text, nullable=False)
    shop_mall_revenue_share_last_7_days = Column(Text, nullable=False)
    shop_mall_revenue_share_last_30_days = Column(Text, nullable=False)
    shop_mall_revenue_share_last_90_days = Column(Text, nullable=False)
    shop_mall_revenue_share_last_180_days = Column(Text, nullable=False)

class Category(Base):
    __tablename__ = 'Category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(Text, nullable=False)
    category_level = Column(Text, nullable=False)
    category_hierarchy = Column(Text, nullable=False)
    revenue_entity_id = Column(Integer, nullable=False)
    live_revenue_entity_id = Column(Integer, nullable=False)
    video_revenue_entity_id = Column(Integer, nullable=False)

    # Category change in revenue
    category_change_in_revenue_yesterday = Column(Text, nullable=False)
    category_change_in_revenue_7_days = Column(Text, nullable=False)
    category_change_in_revenue_30_days = Column(Text, nullable=False)
    category_change_in_revenue_90_days = Column(Text, nullable=False)
    category_change_in_revenue_180_days = Column(Text, nullable=False)

    # Category number of shops
    category_no_of_shops_yesterday = Column(Text, nullable=False)
    category_no_of_shops_7_days = Column(Text, nullable=False)
    category_no_of_shops_30_days = Column(Text, nullable=False)
    category_no_of_shops_90_days = Column(Text, nullable=False)
    category_no_of_shops_180_days = Column(Text, nullable=False)

    # Category revenue growth rate
    category_revenue_growth_rate_yesterday = Column(Text, nullable=False)
    category_revenue_growth_rate_7_days = Column(Text, nullable=False)
    category_revenue_growth_rate_30_days = Column(Text, nullable=False)
    category_revenue_growth_rate_90_days = Column(Text, nullable=False)
    category_revenue_growth_rate_180_days = Column(Text, nullable=False)

    # Category average revenue per shop
    category_avg_revenue_per_shop_yesterday = Column(Text, nullable=False)
    category_avg_revenue_per_shop_7_days = Column(Text, nullable=False)
    category_avg_revenue_per_shop_30_days = Column(Text, nullable=False)
    category_avg_revenue_per_shop_90_days = Column(Text, nullable=False)
    category_avg_revenue_per_shop_180_days = Column(Text, nullable=False)

    # Category top shops revenue ratio
    category_top_3_shops_revenue_ratio_yesterday = Column(Text, nullable=False)
    category_top_3_shops_revenue_ratio_7_days = Column(Text, nullable=False)
    category_top_3_shops_revenue_ratio_30_days = Column(Text, nullable=False)
    category_top_3_shops_revenue_ratio_90_days = Column(Text, nullable=False)
    category_top_3_shops_revenue_ratio_180_days = Column(Text, nullable=False)
    category_top_10_shops_revenue_ratio_yesterday = Column(Text, nullable=False)

    # Category SOA revenue share
    category_soa_revenue_share_yesterday = Column(Text, nullable=False)
    category_soa_revenue_share_7_days = Column(Text, nullable=False)
    category_soa_revenue_share_30_days = Column(Text, nullable=False)
    category_soa_revenue_share_90_days = Column(Text, nullable=False)
    category_soa_revenue_share_180_days = Column(Text, nullable=False)

    # Category affiliate revenue share
    category_aff_revenue_share_yesterday = Column(Text, nullable=False)
    category_aff_revenue_share_7_days = Column(Text, nullable=False)
    category_aff_revenue_share_30_days = Column(Text, nullable=False)
    category_aff_revenue_share_90_days = Column(Text, nullable=False)
    category_aff_revenue_share_180_days = Column(Text, nullable=False)

    # Category mall revenue share
    category_mall_revenue_share_yesterday = Column(Text, nullable=False)
    category_mall_revenue_share_7_days = Column(Text, nullable=False)
    category_mall_revenue_share_30_days = Column(Text, nullable=False)
    category_mall_revenue_share_90_days = Column(Text, nullable=False)
    category_mall_revenue_share_180_days = Column(Text, nullable=False)    

# Many-to-Many relationship tables
class ProductShops(Base):
    __tablename__ = 'Product_Shops'

    shop_name = Column(Text, ForeignKey('Shop.shop_name'), primary_key=True)
    from_shop_name = Column(Text, ForeignKey('Product.from_shop_name'), primary_key=True)

class ProductsVideosCreators(Base):
    __tablename__ = 'Product_Shops'

    from_creator = Column(Text, ForeignKey('Video.from_creator'), primary_key=True)
    on_product = Column(Text, ForeignKey('Video.on_product'), primary_key=True)

    from_creator = Column(Text, ForeignKey('Creator.creator_username'), primary_key=True)
    product_name = Column(Text, ForeignKey('Product.product_name'), primary_key=True)
    video = Column(Text, ForeignKey('Videos.product_name'), primary_key=True)    

class CreatorsProduct(Base):
    __tablename__ = 'Creators_Product'

    creator_id = Column(Integer, ForeignKey('Creator.creator_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.product_id'), primary_key=True)

class ProductVideos(Base):
    __tablename__ = 'Product_Videos'

    product_id = Column(Integer, ForeignKey('Product.product_id'), primary_key=True)
    video_id = Column(Integer, ForeignKey('Video.video_id'), primary_key=True)

class LiveStreamProducts(Base):
    __tablename__ = 'Live_Stream_Products'

    product_id = Column(Integer, ForeignKey('Product.product_id'), primary_key=True)
    live_stream_id = Column(Integer, ForeignKey('Live_Stream.live_stream_id'), primary_key=True)

class ShopLiveStreams(Base):
    __tablename__ = 'Shop_Live_Streams'

    shop_id = Column(Integer, ForeignKey('Shop.shop_id'), primary_key=True)
    live_stream_id = Column(Integer, ForeignKey('Live_Stream.live_stream_id'), primary_key=True)

class ShopCreator(Base):
    __tablename__ = 'Shop_Creator'

    shop_id = Column(Integer, ForeignKey('Shop.shop_id'), primary_key=True)
    creator_id = Column(Integer, ForeignKey('Creator.creator_id'), primary_key=True)

class CreatorLiveStreams(Base):
    __tablename__ = 'Creator_Live_Streams'

    creator_id = Column(Integer, ForeignKey('Creator.creator_id'), primary_key=True)
    live_stream_id = Column(Integer, ForeignKey('Live_Stream.live_stream_id'), primary_key=True)


















# CREATE TABLE Product (
#    product_id SERIAL PRIMARY KEY,
#    product_name TEXT NOT NULL,
#    shipped_from TEXT NOT NULL,
#    product_category TEXT NOT NULL,
#    tiktok_product_link TEXT NOT NULL,
#    product_price TEXT NOT NULL,
#    lowest_price_30_days TEXT NOT NULL,
#    product_earliest_date_recorded TEXT NOT NULL,
#    from_shop_name TEXT NOT NULL,
#    image_links TEXT NOT NULL,
#    revenue_entity_id INT NOT NULL,
#    video_revenue_entity_id INT NOT NULL,
#    live_revenue_entity_id INT NOT NULL,
#    avg_unit_price_entity_id INT NOT NULL,
#    item_sold_entity_id INT NOT NULL,
#    mall_revenue_entity_id INT NOT NULL
# );

# CREATE TABLE Creator (
#    creator_id SERIAL PRIMARY KEY,
#    creator_username TEXT NOT NULL,
#    no_of_followers TEXT NOT NULL,
#    debut_time TEXT NOT NULL,
#    last_30_days_products INT NOT NULL,
#    creator_bio TEXT NOT NULL,
#    tiktok_link TEXT,
#    instagram_link TEXT,
#    contact_email_address TEXT,
#    creator_earliest_date_recorded TEXT NOT NULL,
#    revenue_entity_id INT NOT NULL,
#    live_revenue_entity_id INT NOT NULL,
#    video_revenue_entity_id INT NOT NULL,
#    avg_unit_price_entity_id INT NOT NULL,
#    traffic_live_views_yesterday TEXT NOT NULL,
#    traffic_live_views_per_day_last_7_days TEXT NOT NULL,
#    traffic_live_views_per_day_last_30_days TEXT NOT NULL,
#    traffic_live_views_per_day_last_90_days TEXT NOT NULL,
#    traffic_live_views_per_day_last_180_days TEXT NOT NULL,
#    traffic_live_views_last_7_days TEXT NOT NULL,
#    traffic_live_views_last_30_days TEXT NOT NULL,
#    traffic_live_views_last_90_days TEXT NOT NULL,
#    traffic_live_views_last_180_days TEXT NOT NULL,
#    video_views_yesterday TEXT NOT NULL,
#    video_views_per_day_last_7_days TEXT NOT NULL,
#    video_views_per_day_last_30_days TEXT NOT NULL,
#    video_views_per_day_last_90_days TEXT NOT NULL,
#    video_views_per_day_last_180_days TEXT NOT NULL,
#    video_views_last_7_days TEXT NOT NULL,
#    video_views_last_30_days TEXT NOT NULL,
#    video_views_last_90_days TEXT NOT NULL,
#    video_views_last_180_days TEXT NOT NULL,
#    new_followers_yesterday TEXT NOT NULL,
#    new_followers_per_day_last_7_days TEXT NOT NULL,
#    new_followers_per_day_last_30_days TEXT NOT NULL,
#    new_followers_per_day_last_90_days TEXT NOT NULL,
#    new_followers_per_day_last_180_days TEXT NOT NULL,
#    new_followers_last_7_days TEXT NOT NULL,
#    new_followers_last_30_days TEXT NOT NULL,
#    new_followers_last_90_days TEXT NOT NULL,
#    new_followers_last_180_days TEXT NOT NULL
# );

# CREATE TABLE Video (
#    video_id SERIAL PRIMARY KEY,
#    video_link TEXT NOT NULL,
#    video_tags TEXT,
#    video_music_info TEXT,
#    revenue_entity_id INT NOT NULL,
#    video_revenue_entity_id INT NOT NULL,
#    item_sold_entity_id INT NOT NULL,
#    video_publish_date TEXT NOT NULL,
#    video_duration TEXT NOT NULL,
#    video_advertising_information TEXT,
#    video_earliest_date_recorded TEXT NOT NULL,
#    video_views_yesterday TEXT NOT NULL,
#    video_views_per_day_last_7_days TEXT NOT NULL,
#    video_views_per_day_last_30_days TEXT NOT NULL,
#    video_views_per_day_last_90_days TEXT NOT NULL,
#    video_views_per_day_last_180_days TEXT NOT NULL,
#    video_views_last_7_days TEXT NOT NULL,
#    video_views_last_30_days TEXT NOT NULL,
#    video_views_last_90_days TEXT NOT NULL,
#    video_views_last_180_days TEXT NOT NULL,
#    video_new_followers_yesterday TEXT NOT NULL,
#    video_new_followers_per_day_last_7_days TEXT NOT NULL,
#    video_new_followers_per_day_last_30_days TEXT NOT NULL,
#    video_new_followers_per_day_last_90_days TEXT NOT NULL,
#    video_new_followers_per_day_last_180_days TEXT NOT NULL,
#    video_new_followers_last_7_days TEXT NOT NULL,
#    video_new_followers_last_30_days TEXT NOT NULL,
#    video_new_followers_last_90_days TEXT NOT NULL,
#    video_new_followers_last_180_days TEXT NOT NULL,
#    video_ad_view_ratio_yesterday TEXT NOT NULL,
#    video_ad_view_ratio_last_7_days TEXT NOT NULL,
#    video_ad_view_ratio_last_30_days TEXT NOT NULL,
#    video_ad_view_ratio_last_90_days TEXT NOT NULL,
#    video_ad_view_ratio_last_180_days TEXT NOT NULL,
#    video_ad_revenue_ratio_yesterday TEXT NOT NULL,
#    video_ad_revenue_ratio_last_7_days TEXT NOT NULL,
#    video_ad_revenue_ratio_last_30_days TEXT NOT NULL,
#    video_ad_revenue_ratio_last_90_days TEXT NOT NULL,
#    video_ad_revenue_ratio_last_180_days TEXT NOT NULL,
#    video_ad_spend_yesterday TEXT NOT NULL,
#    video_ad_spend_last_7_days TEXT NOT NULL,
#    video_ad_spend_last_30_days TEXT NOT NULL,
#    video_ad_spend_last_90_days TEXT NOT NULL,
#    video_ad_spend_last_180_days TEXT NOT NULL,
#    video_ad_roas_yesterday TEXT NOT NULL,
#    video_ad_roas_last_7_days TEXT NOT NULL,
#    video_ad_roas_last_30_days TEXT NOT NULL,
#    video_ad_roas_last_90_days TEXT NOT NULL,
#    video_ad_roas_last_180_days TEXT NOT NULL
# );

# CREATE TABLE Live_Stream (
#    live_stream_id SERIAL PRIMARY KEY,
#    live_stream_name TEXT,
#    live_stream_product_count TEXT NOT NULL,
#    live_revenue_entity_id INT NOT NULL,
#    avg_unit_price_entity_id INT NOT NULL,
#    item_sold_entity_id INT NOT NULL,
#    live_stream_top_3_category TEXT NOT NULL,
#    live_stream_time TEXT NOT NULL,
#    live_stream_duration TEXT NOT NULL,
#    live_stream_creator TEXT NOT NULL,
#    live_stream_online_viewers TEXT NOT NULL,
#    live_stream_online_viewers_per_minute TEXT NOT NULL,
#    live_stream_views TEXT NOT NULL,
#    live_stream_views_per_minute TEXT NOT NULL,
#    live_stream_item_sold TEXT NOT NULL,
#    live_stream_item_sold_per_minute TEXT NOT NULL
# );

# CREATE TABLE Shop (
#    shop_id SERIAL PRIMARY KEY,
#    shop_name TEXT NOT NULL,
#    shop_type TEXT NOT NULL,
#    shop_earliest_date_recorded TEXT NOT NULL,
#    revenue_entity_id INT NOT NULL,
#    avg_unit_price_entity_id INT NOT NULL,
#    item_sold_entity_id INT NOT NULL,
#    mall_revenue_entity_id INT NOT NULL,
#    shop_soa_revenue_yesterday TEXT NOT NULL,
#    shop_soa_revenue_per_day_last_7_days TEXT NOT NULL,
#    shop_soa_revenue_per_day_last_30_days TEXT NOT NULL,
#    shop_soa_revenue_per_day_last_90_days TEXT NOT NULL,
#    shop_soa_revenue_per_day_last_180_days TEXT NOT NULL,
#    shop_soa_revenue_last_7_days TEXT NOT NULL,
#    shop_soa_revenue_last_30_days TEXT NOT NULL,
#    shop_soa_revenue_last_90_days TEXT NOT NULL,
#    shop_soa_revenue_last_180_days TEXT NOT NULL,
#    shop_affiliate_revenue_yesterday TEXT NOT NULL,
#    shop_affiliate_revenue_per_day_last_7_days TEXT NOT NULL,
#    shop_affiliate_revenue_per_day_last_30_days TEXT NOT NULL,
#    shop_affiliate_revenue_per_day_last_90_days TEXT NOT NULL,
#    shop_affiliate_revenue_per_day_last_180_days TEXT NOT NULL,
#    shop_affiliate_revenue_last_7_days TEXT NOT NULL,
#    shop_affiliate_revenue_last_30_days TEXT NOT NULL,
#    shop_affiliate_revenue_last_90_days TEXT NOT NULL,
#    shop_affiliate_revenue_last_180_days TEXT NOT NULL,
#    shop_soa_revenue_share_yesterday TEXT NOT NULL,
#    shop_soa_revenue_share_last_7_days TEXT NOT NULL,
#    shop_soa_revenue_share_last_30_days TEXT NOT NULL,
#    shop_soa_revenue_share_last_90_days TEXT NOT NULL,
#    shop_soa_revenue_share_last_180_days TEXT NOT NULL,
#    shop_aff_revenue_share_yesterday TEXT NOT NULL,
#    shop_aff_revenue_share_last_7_days TEXT NOT NULL,
#    shop_aff_revenue_share_last_30_days TEXT NOT NULL,
#    shop_aff_revenue_share_last_90_days TEXT NOT NULL,
#    shop_aff_revenue_share_last_180_days TEXT NOT NULL,
#    shop_mall_revenue_share_yesterday TEXT NOT NULL,
#    shop_mall_revenue_share_last_7_days TEXT NOT NULL,
#    shop_mall_revenue_share_last_30_days TEXT NOT NULL,
#    shop_mall_revenue_share_last_90_days TEXT NOT NULL,
#    shop_mall_revenue_share_last_180_days TEXT NOT NULL
# );

# CREATE TABLE Product_Shops (
#    shop_id INT REFERENCES Shop(shop_id),
#    product_id INT REFERENCES Product(product_id),
#    PRIMARY KEY (shop_id, product_id)
# );

# CREATE TABLE Creators_Product (
#    creator_id INT REFERENCES Creator(creator_id),
#    product_id INT REFERENCES Product(product_id),
#    PRIMARY KEY (creator_id, product_id)
# );

# CREATE TABLE Product_Videos (
#    product_id INT REFERENCES Product(product_id),
#    video_id INT REFERENCES Video(video_id),
#    PRIMARY KEY (product_id, video_id)
# );

# CREATE TABLE Live_Stream_Products (
#    product_id INT REFERENCES Product(product_id),
#    live_stream_id INT REFERENCES Live_Stream(live_stream_id),
#    PRIMARY KEY (product_id, live_stream_id)
# );

# CREATE TABLE Shop_Live_Streams (
#    shop_id INT REFERENCES Shop(shop_id),
#    live_stream_id INT REFERENCES Live_Stream(live_stream_id),
#    PRIMARY KEY (shop_id, live_stream_id)
# );

# CREATE TABLE Shop_Creator (
#    shop_id INT REFERENCES Shop(shop_id),
#    creator_id INT REFERENCES Creator(creator_id),
#    PRIMARY KEY (shop_id, creator_id)
# );

# CREATE TABLE Creator_Live_Streams (
#    creator_id INT REFERENCES Creator(creator_id),
#    live_stream_id INT REFERENCES Live_Stream(live_stream_id),
#    PRIMARY KEY (creator_id, live_stream_id)
# );
