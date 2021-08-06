
# =========================================
import pandas as pd 
path= "./data/"
csv_2021= "seoul_rental_2021.txt"
csv_2020= "seoul_rental_2020.csv"
csv_2019= "seoul_rental_2019.csv"
csv_2018= "seoul_rental_2018.csv"
csv_2017= "seoul_rental_2017.csv"
csv_2016= "seoul_rental_2016.txt"
csv_2015= "seoul_rental_2015.txt"
# csv_2014= "seoul_rental_2014.txt"
csv_2014_clean= "seoul_rental_2014_clean.txt"
csv_2013= "seoul_rental_2013.txt"
csv_2012= "seoul_rental_2012.txt"
csv_2011= "seoul_rental_2011.txt"


# pd.read_csv(skiprows=15)
# to skip the first 15 rows

df_2021= pd.read_csv(path+csv_2021,encoding="utf-8")
# df_2021.shape
df_2020= pd.read_csv(path+csv_2020,encoding="cp949")
df_2019= pd.read_csv(path+csv_2019,encoding="cp949")
df_2018= pd.read_csv(path+csv_2018,encoding="cp949")
df_2017= pd.read_csv(path+csv_2017,encoding="cp949")
df_2016= pd.read_csv(path+csv_2016,encoding="utf-8")
df_2015= pd.read_csv(path+csv_2015,encoding="utf-8")
# df_2014= pd.read_csv(path+csv_2014,encoding="utf-8")
df_2014_clean= pd.read_csv(path+csv_2014_clean,encoding="utf-8")
# df_2014_clean.shape
df_2013= pd.read_csv(path+csv_2013,encoding="utf-8")
df_2012= pd.read_csv(path+csv_2012,encoding="utf-8")
df_2011= pd.read_csv(path+csv_2011,encoding="utf-8")


# =======================================================
# Merge 10-year records into one dataframe
# - Check the shape of all the dataframes

# df_list= [df_2020,df_2019,df_2018,df_2017,df_2016,df_2015,df_2014,df_2013,df_2012,df_2011]
# for i,df in enumerate(df_list):
#     year=2020-i
#     print(year,":",df.shape)
# print("="*35)


df_list= [df_2021,df_2020,df_2019,df_2018,df_2017,df_2016,df_2015,df_2014_clean,df_2013,df_2012,df_2011]
for i,df in enumerate(df_list):
    year=2020-i
    print(year,":",df.shape)

df= pd.concat(df_list,ignore_index=True)
df.shape


### Rename data columns
#### - 시군구 → district1
#### - 번지 → lot_num
#### - 본번 → lot_num_1
#### - 부번 → lot_num_2
#### - 단지명 → estate_name
#### - 전월세구분 → rent_type (lump-sum or monthly)
#### - 전용면적(㎡) → unit_size (m²)
#### - 계약년월 → sign_yymm
#### - 계약일 → sign_dd
#### - 보증금(만원) → deposit (in 10,000 won)
#### - 월세(만원) → pay_monthly (in 10,000 won)
#### - 층 → floor
#### - 건축년도 → yr_built
#### - 도로명 → str_addr

cols= ["district1","lot_num","lotnum_1","lotnum_2","estate_name","rent_type","unit_size","sign_yymm","sign_dd","deposit","pay_monthly","floor","yr_built","str_addr"]

df.columns= cols

# =======================================================
### Fill in empty or whitespaced cells with estate_name
#### 🇰🇷
#### > 탐색 결과 도로명 컬럼에 whitespace만 있는 row가 파일마다 수천개 발견됨. 빈 cell은 단지명으로 채움

# Of 32419 cells of length 1,
# - 32418 cells has one whitespace,
# 🇰🇷 도로 주소가 없는 " " 셀에 단지명을 채워넣음.
# 32418 rows 
df["estate_name"]= df.estate_name.astype(str)
df["str_addr"]= df.str_addr.astype(str)
idx= df[(df.str_addr.str.len()==1)&(df.str_addr==" ")].index # idx.shape
df.loc[idx,"str_addr"]= df.iloc[idx].estate_name
df.iloc[idx].str_addr

#### and the remaining one cell has the value of "5"; will be filled manually with its street address 
# index 166852, current str_addr: "5"
# manually change it to "선유로11길 5"
idx_one= df[(df.str_addr.str.len()==1)&(df.str_addr!=" ")].index # idx.shape
df.loc[idx_one,"str_addr"]= "선유로11길 "+df.iloc[idx_one].str_addr.str[0]

# =========================
### Drop unused columns
#### - lot_num
#### - lot_num_2
#### - estate_name
#### - str_addr
df.drop(["lot_num","lotnum_2","estate_name"],axis=1,inplace=True)
# df.head(1)

# =========================
### New column district
#### - 전체 데이터가 서울 지역에 한정되어 있으므로 "서울특별시", 동 이름 제거
df.insert(0,"district",[val.split()[1] for i,val in df.district1.iteritems() ])
# df.head(1)

df.insert(1,"old_div",[f"{val.split()[2]}" for i,val in df.district1.iteritems()])

# ===========================
### Drop columns
#### - district1
df.drop("district1",axis=1,inplace=True)
df.head(1)

# ==============================
### Create new column sign_date
#### - create `sign_date` from sign_yymm and sign_dd
#### 🇰🇷
#### > 계약년월(예: 202004)과 계약일(11)을 합쳐 sign_date (예: 2020-04-11) 생성
sign_date= pd.to_datetime((df.sign_yymm.astype(str)+df.sign_dd.astype(str)),format="%Y%m%d")
df.insert(7,"sign_date",sign_date)
df.head(1)

# ===================================
### Change dtype of `deposit` to int
#### - First, remove the thousand-separator
#### - and convert to int
#### 🇰🇷 
#### > 보증금 컬럼의 구분자(,)를 제거하고 dtype을 int로 변환
df.deposit.astype(str).str.contains(",").sum()
# df["deposit"]= df_backup["보증금(만원)"]
df["deposit"]= df.deposit.astype(str).str.replace(",","").astype(int) # 2125 => 1806 unique values

### =================================================
### Change dtype of `lotnum_1`,`sign_yymm`,`sign_dd`,`rent_price`,`floor` to int32
#### 🇰🇷 
#### > dtype을 int32/float32로 변환하며 memory usage ↓
import numpy as np
df.lotnum_1= df.lotnum_1.astype(int)
df.sign_yymm= df.sign_yymm.astype(int)
df.sign_dd= df.sign_dd.astype(int)
df.unit_size= df.unit_size.astype(np.float32)
df.pay_monthly= df.pay_monthly.astype(int)
df.floor= df.floor.astype(int)


# ======================================
## FEATURE ENGINEERING
### GPS coordinates for the 25 districts
### - ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구',       '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구',       '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']

coords= [
    (37.5172, 127.0473), #gangnam
    (37.5301, 127.1238), #gangdong
    (37.6396, 127.0257), #gangbuk-gu
    (37.5510, 126.8495),# gangseo-gu
    (37.4784, 126.9516),# gwanak-gu
    (37.5385, 127.0823), #gwangjin-gu 
    (37.4954, 126.8874), #guro-gu
    (37.4519, 126.9020), #geumcheon-gu
    (37.6542, 127.0568), #nowon-gu
    (37.6688, 127.0471), #dobong-gu
(37.5744, 127.0400), #dongdaemun-gu
(37.5124, 126.9393), #dongjak-gu
(37.5638, 126.9084), #mapo-gu
(37.5791, 126.9368), #seodaemun-gu
(37.4837, 127.0324), #seocho-gu
(37.5633, 127.0371), #seongdong-gu
(37.5891, 127.0182), #seongbuk-gu
(37.5145, 127.1066), #songpa-gu
(37.5169, 126.8664), #yangcheon-gu
(37.5264, 126.8962), #yeongdeungpo-gu
    (37.5384, 126.9654), #yongsan-gu
    (37.6027, 126.9291), #eunpyeong-gu
    (37.5730, 126.9794), #jongno-gu
    (37.5641, 126.9979), #jung-gu
    (37.6066, 127.0927), #jungnang-gu
]

DISTRICT_LAT= {}
DISTRICT_LON= {}
for idx,name in enumerate((list(df.district.unique()))):
    DISTRICT_LAT[name]= coords[idx][0]
    DISTRICT_LON[name]= coords[idx][1]

### Add latitude and longitude columns
lat= [DISTRICT_LAT.get(name) for i,name in df["district"].iteritems()]
lon= [DISTRICT_LON.get(name) for i,name in df["district"].iteritems()]

df.insert(1,"latitude",lat)
df.insert(2,"longitude",lon)
df.head(1)

#
# =================================
# Add new `street` column
# separator: whitespace

dict_lot_num_street= {}
dict_lot_num_street["669-3"]= "방학로 173"
dict_lot_num_street["121-5"]= "동소문로24길 13-9"
dict_lot_num_street["441-11"]= "고덕로 45"
dict_lot_num_street["204-5"]= "자곡로 127"
dict_lot_num_street["9-13"]= "양천로57길 9-13"
dict_lot_num_street["115-1"]= "마곡서1로 115-1"
dict_lot_num_street["10-16"]= "중앙로 10-16"
dict_lot_num_street["16"]= "선릉로89길 16"
dict_lot_num_street["355"]= "아차산로 355"
dict_lot_num_street["164"]= "사당로 164"
dict_lot_num_street["212"]= "올림픽로 212"

dict_lot_num_street["한흥 삼성오피스텔"]= "봉은사로 430"
dict_lot_num_street["한흥삼성오피스텔"]= "봉은사로 430"
dict_lot_num_street["강남 드림하이 오피스텔"]= "헌릉로569길 21-30"
dict_lot_num_street["강남드림하이오피스텔"]= "헌릉로569길 21-30"
dict_lot_num_street["역삼 푸르지오 시티"]= "논현로85길 52"
dict_lot_num_street["역삼푸르지오시티"]= "논현로85길 52"
dict_lot_num_street["강일 포디움"]= "아리수로91길 24-9"
dict_lot_num_street["강일포디움"]= "아리수로91길 24-9"
dict_lot_num_street["에코 타워빌"]= "성안로27길 51-14"
dict_lot_num_street["에코타워빌"]= "성안로27길 51-14"
dict_lot_num_street["GM Valley"]= "곰달래로 116"
dict_lot_num_street["GMValley"]= "곰달래로 116"
dict_lot_num_street["금천 롯데캐슬 골드파크 2차"]= "벚꽃로 30"
dict_lot_num_street["금천롯데캐슬골드파크2차"]= "벚꽃로 30"
dict_lot_num_street["도봉 엠블렘"]= "도봉로180길 38"
dict_lot_num_street["도봉엠블렘"]= "도봉로180길 38"
dict_lot_num_street["도봉 투웨니퍼스트 1단지"]= "도봉로180길 20"
dict_lot_num_street["도봉투웨니퍼스트1단지"]= "도봉로180길 20"
dict_lot_num_street["도봉 투웨니퍼스트 2단지"]= "도봉로180길 28"
dict_lot_num_street["도봉투웨니퍼스트2단지"]= "도봉로180길 28"
dict_lot_num_street["창동 투웨니퍼스트"]= "도봉로110라길 70-14"
dict_lot_num_street["창동투웨니퍼스트"]= "도봉로110라길 70-14"


# manually add street names through lookup
csv_str_name= "addresses_without_street_info_new.csv"
lotnum_to_street= pd.read_csv(path+csv_str_name)
lotnum_to_street.street= lotnum_to_street.street.apply(lambda x: x.strip())

# update DICT_LOT_NUM_STREET
add_to_dict= dict(zip(lotnum_to_street["str_addr"],lotnum_to_street["street"]))
dict_lot_num_street.update(add_to_dict)
# dict_lot_num_street

import re
df.str_addr= df.str_addr.apply(lambda x: x.strip())
df.str_addr= df.str_addr.apply(lambda x: x if dict_lot_num_street.get(x)==None else dict_lot_num_street.get(x)) # get value of x, if none keep it

# import numpy as np
# np.argmin(str_addr.str.len())

ser_street= [re.split("\s",val)[0] for val in df.str_addr.values]
#### longest street name
# max(ser_street,key=len) # 목동중앙북로

### Add new `street` column
# del df["street"]
df.insert(3,"street",ser_street)
# df.head(1)

# =================================
# MANUALLY CORRECT STREET NAMES
# load address_conflict_corr.csv
csv_str_name= "str_name_conflicts_corr.csv"
lotnum_to_street= pd.read_csv(path+csv_str_name)
dict_str_name_2= dict(zip(lotnum_to_street.old_div+" "+lotnum_to_street.lotnum_1.astype(str),lotnum_to_street.street.str.strip()))

# update "street" of df
def update_street(old_div,lotnum,street):
    # old_div: pd.series
    # lotnum: pd.series
    # street: pd.series
    # dict_str: dict
    key= old_div+" "+str(lotnum)
    street_upd= street if dict_str_name_2.get(key)==None else dict_str_name_2.get(key)
    return street_upd

street_update= df[["old_div","lotnum_1","street"]].apply(lambda x: update_street(*x),axis=1)

df["street"]= street_update

# =========================================
# create geometry from (latitude,longitude)
import geopandas as gpd
# gpd.__version__
from shapely.geometry import Point
geometry= [Point(xy) for xy in zip(df.longitude,df.latitude)]
gdf= gpd.GeoDataFrame(df,geometry=geometry)
gdf.set_crs(epsg=3857,inplace=True)
gdf.crs

# ========================
# add ID column
ids= gdf.index.tolist()
gdf.insert(0,"id",ids)

# =======================
# LOAD SEOUL DISTRICT MAP
#
import geopandas as gpd
path_geo= "./data/seoul_districts/"
filename= "LARD_ADM_SECT_SGG_11.shp"
seoul_dists= gpd.read_file(path_geo+filename,encoding="cp949")
seoul_dists.crs

# =========================
# LOAD SEOUL STREET MAP
path_geo= "./data/seoul_streets/"
filename= "Z_KAIS_TL_SPRD_MANAGE_11000.shp"
seoul_streets= gpd.read_file(path_geo+filename,encoding="cp949")
seoul_streets.crs

# SIG_CD: administrative district code
# RN_CD: road code
# RN: road name
# ENG_RN: road name in English
#
# keep only the columns below
street_cols= ["SIG_CD","RN_CD","RN","ENG_RN","geometry"]
seoul_streets= seoul_streets[street_cols]

# rename columns
street_cols= ["dist_code","str_code","str_name","str_name_en","geometry"]
seoul_streets.columns= street_cols

# drop duplicate rd_code
seoul_streets.drop_duplicates("str_code",inplace=True)

# convert coord. system to epsg:3857 (google/bing/yahoo,osm maps)
# The most common CRS for online maps
# CRS: coordinate reference system
seoul_dists= seoul_dists.to_crs(epsg=3857)
seoul_dists.crs

# change column names
# ['ADM_SECT_C', 'SGG_NM', 'SGG_OID', 'COL_ADM_SE', 'GID', 'geometry']
seoul_dists.columns= ["dist_code","SGG_NM", 'SGG_OID', 'COL_ADM_SE', 'GID', 'geometry']

# untidy cells of SGG_NM: 
# 서울시노원구,서울시성북구,서울시도봉구
seoul_dists.SGG_NM= seoul_dists.SGG_NM.astype(str).apply(lambda x: re.sub("서울시","",x))

# =================================
# MERGE GDF_DISTRICT WITH MAP_SEOUL
drop_cols= ["latitude","longitude","old_div","lotnum_1","sign_yymm","sign_dd","geometry"] # drop Point geometry
gdf_seoul_dist= pd.merge(seoul_dists[['dist_code', 'SGG_NM', 'geometry']],df.drop(drop_cols,axis=1),how="right",left_on="SGG_NM",right_on="district")

# drop SGG_NM column
gdf_seoul_dist.drop(["SGG_NM"],axis=1,inplace=True)

# =========================
# ADD STR_CODE TO GDF_SEOUL_DIST
# left_df.merge(right_df, on='user_id', how='left')

gdf_seoul_dist.insert(4,"str_code",0)
dict_str_code= dict(zip(seoul_streets.str_name,seoul_streets.str_code))

def fill_str_code(street,rd_code):
    str_code= 0 if dict_str_code.get(street)==None else dict_str_code.get(street)
    return str_code

# street names still incorrect: 43642 rows
gdf_seoul_dist.street= gdf_seoul_dist.street.apply(lambda x: re.split("\s",x)[0])

gdf_seoul_dist.str_code= gdf_seoul_dist[["street","str_code"]].apply(lambda x: fill_str_code(*x),axis=1)
gdf_seoul_dist.shape

# drop rows
# 734 records without street code
# 38 unique addrs 
gdf_seoul_dist[gdf_seoul_dist.str_code==0][["str_code","street","str_addr"]].drop_duplicates()

drop_cols= ["str_addr"]
gdf_seoul_dist= gdf_seoul_dist[gdf_seoul_dist.str_code!=0].drop(drop_cols,axis=1)
gdf_seoul_dist.shape
# 314629 - 501 = 313895 rows
# (313895, 13)

# ============================================
# GeoDataFrame with street LineString geometry
seoul_streets.columns= ['dist_code', 'str_code', 'str_name', 'str_name_en', 'geometry']
seoul_streets.dist_code= seoul_streets.dist_code.astype(int)
seoul_streets.str_code= seoul_streets.str_code.astype(int)

gdf_seoul_dist.str_code= gdf_seoul_dist.str_code.astype(int)

# ['id', 'district', 'str_code', 'street','rent_type', 'unit_size', 'sign_date', 'deposit', 'pay_monthly','floor', 'yr_built']
gdf_seoul_strt= pd.merge(seoul_streets[['dist_code', 'str_code', 'str_name_en', 'geometry']],gdf_seoul_dist[['id', 'district', 'str_code', 'street','rent_type', 'unit_size', 'sign_date', 'deposit', 'pay_monthly','floor', 'yr_built']],on="str_code") 
gdf_seoul_strt.head(1)

# ===============================================
# DISTRICT STATS
# 1. size_per_district_df:
#                        unit size stats per district
# 2. r_type_ratio_dist_df:
#                        rent_type_ratio per dist
# 3. deposit_per_dist
# 4. rent_per_dist
# 5. yr_built_per_dist
# 6. floor_per_dist

# =======================
# UNIT_SIZE BY DISTRICT
# average, mode, maximum
size_per_district_df= gdf_seoul_dist.groupby("district")["unit_size"].agg(size_avg="mean",size_median="median",size_freq=lambda x:x.value_counts().index[0],size_max="max").sort_values(by="size_median",ascending=False)

# =======================
# RENT_TYPE BY DISTRICT
# count, ratio

print(df.rent_type[-5:])
# convert string to boolean: lump-sum 0, monthly 1
gdf_seoul_dist["rent_type"]= pd.factorize(gdf_seoul_dist["rent_type"])[0].astype(bool).astype(int)
gdf_seoul_dist.dtypes
gdf_seoul_dist.rent_type[-5:]

r_type_per_dist_df= gdf_seoul_dist.groupby("district")["rent_type"].value_counts().unstack().sort_values(by=1,ascending=False).rename(columns={0:"전세",1:"월세"}) # 1: monthly

type_1_ratio= r_type_per_dist_df["월세"]/gdf_seoul_dist.district.value_counts()*100
type_2_ratio= r_type_per_dist_df["전세"]/gdf_seoul_dist.district.value_counts()*100

r_type_ratio_dist_df= pd.DataFrame(
    {"monthly_count":r_type_per_dist_df["월세"],
     "monthly_ratio":type_1_ratio,
     "lumpsum_count":r_type_per_dist_df["전세"],
    "lumpsum_ratio":type_2_ratio},index=type_1_ratio.index
).sort_values(by="monthly_count",ascending=False)

# =======================
# DEPOSIT BY DISTRICT
# average, mode, maximum
deposit_per_dist= gdf_seoul_dist.groupby("district")["deposit"].agg(deposit_avg="mean",deposit_median="median",deposit_freq=lambda x:x.value_counts().index[0],deposit_max="max").sort_values(by="deposit_avg",ascending=False)

# =======================
# MONTHLY RENT BY DISTRICT
# "월세" average, mdoe, maximum
# 0: lump-sum | 1: monthly
rent_per_dist= gdf_seoul_dist[gdf_seoul_dist.rent_type==1].groupby("district")["pay_monthly"].agg(rent_avg="mean",rent_median="median",rent_freq=lambda x:x.value_counts().index[0],rent_max="max").sort_values(by="rent_avg",ascending=False)

# =======================
# YR_BUILT BY DISTRICT
# median, mode, maximum
# gdf_map["yr_built"]= df_backup["건축년도"]
yr_built_per_dist= gdf_seoul_dist[gdf_seoul_dist.yr_built.notna()].groupby("district")["yr_built"].agg(yr_built_median="median",yr_built_freq=lambda x:x.value_counts().index[0],yr_built_max="max").sort_values(by="yr_built_median",ascending=False)

### Data imputation: yr_built
#### - Fill empty cells of yr_built with the median value
#### 🇰🇷 - 건축년도가 비어 있는 경우 median value로 채움

#### find the median value for a given column
def find_median(district):
    # district,yr_built
    return yr_built_per_dist.loc[yr_built_per_dist.index==district,"yr_built_median"].astype(int)[0]

# df.loc[df.yr_built.isna(),"yr_built"]= find_median("yr_built", df) # median: 2013
gdf.loc[gdf.yr_built.isna(),"yr_built"]= gdf.loc[gdf.yr_built.isna(),"district"].apply(lambda x:find_median(x))

gdf_seoul_dist.loc[gdf_seoul_dist.yr_built.isna(),"yr_built"]= gdf_seoul_dist.loc[gdf_seoul_dist.yr_built.isna(),"district"].apply(lambda x:find_median(x))

# AFTER IMPUTATION
# overwrite yr_built statistics by district
gdf_seoul_dist.yr_built= gdf_seoul_dist.yr_built.astype(int)
yr_built_per_dist= gdf_seoul_dist.groupby("district")["yr_built"].agg(yr_built_median="median",yr_built_freq=lambda x:x.value_counts().index[0],yr_built_max="max").sort_values(by="yr_built_median",ascending=False)

# =======================
# Floor by district
# median, mode, max
floor_per_dist= gdf_seoul_dist.groupby("district")["floor"].agg(floor_median="median",floor_freq=lambda x:x.value_counts().index[0],floor_max="max").sort_values(by="floor_max",ascending=False)


# merge district stats dataframes
col_dists= [size_per_district_df,r_type_ratio_dist_df,deposit_per_dist,rent_per_dist,yr_built_per_dist,floor_per_dist]
df_dists= pd.concat(col_dists,axis=1)
df_dists.shape # (25, 22)

# For plotting
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import seaborn as sns 
from mpl_toolkits.axes_grid1 import make_axes_locatable


# change dtypes to category for discrete variables
gdf_seoul_dist["dist_code"]= gdf_seoul_dist.dist_code.astype(np.int32)
gdf_seoul_dist["district"]= gdf_seoul_dist.district.astype("category")
gdf_seoul_dist["street"]= gdf_seoul_dist.street.astype("category")
gdf_seoul_dist["str_code"]= gdf_seoul_dist.str_code.astype(np.int32)
gdf_seoul_dist.dtypes


# ======================================
# EDA

# PLOT
# yearly rental volume
gdf_seoul_dist["year"]= gdf_seoul_dist.sign_date.dt.year

dist_en= ['Gang-nam',
 'Gang-dong',
 'Gang-buk',
 'Gang-seo',
 "Gwan-ak",
 'Gwang-jin',
 'Guro',
 'Geum-cheon',
 'Nowon',
 'Dobong',
 'Dong-daemun',
 'Dong-jak',
 'Mapo',
 'Seo-daemun',
 'Seo-cho',
 'Seong-dong',
 'Seong-buk',
 'Song-pa',
 'Yang-cheon',
 'Young-deungpo',
 'Yongsan',
 'Eun-pyeong',
 'Jong-no',
 'Jung-gu',
 'Jung-nang']
plt.figure(figsize=(20,15))
plt.style.use("fivethirtyeight")
fig,ax= plt.subplots()
ax= sns.countplot(x="year",data=gdf_seoul_dist,ax=ax) #,hue="year"

# ax.set_xticklabels(dist_en,fontsize=14)#,              fontproperties=custom_font
# ax.set_ylabel("Count",fontsize=16)
# ax.set_xlabel("District",fontsize=16)
fig.autofmt_xdate()

plt.title("Yearly Rental Volume",fontsize=18)
plt.savefig("02_yearly_rental_vol.png")
plt.show()

# PLOT
# yearly rental volume by rent_type
plt.figure(figsize=(20,15))
plt.style.use("fivethirtyeight")
fig,ax= plt.subplots()
g= sns.countplot(x="year",hue="rent_type",data=gdf_seoul_dist,ax=ax) #

new_labels = ['lump-sum', 'monthly']
g.legend(new_labels)
# replace labels
# g.legend_.set_label(new_labels)
# ax.set_xticklabels(dist_en,fontsize=14)#,              fontproperties=custom_font
# ax.set_ylabel("Count",fontsize=16)
# ax.set_xlabel("District",fontsize=16)
fig.autofmt_xdate()

plt.title("Yearly Rental Volume by Type",fontsize=18)
plt.savefig("02_yearly_rental_vol_by_rent_type.png")
plt.show()


# ==========================================
fig,ax= plt.subplots(1,1,figsize=(20,8))
divider= make_axes_locatable(ax)
cax= divider.append_axes("right", size="5%",pad=.1)

gdf_seoul_dist.drop_duplicates("district").plot((district_ratio/gdf_seoul_dist.shape[0]*100).values,ax=ax,legend=True,cax=cax,edgecolor="black",cmap="cubehelix_r")
ax.set_title("Rentals (%) by District")
ax.set_axis_off()
plt.show()

# ================================
# GEOPLOT
# coord system: 4326, google earth
district_ratio= gdf_seoul_dist.district.value_counts()
df_district_ratio= pd.DataFrame({"rental_vol":district_ratio,"rental_ratio":(district_ratio/gdf_seoul_dist.shape[0]*100)},index=district_ratio.index)

seoul_ge= gdf_seoul_dist.drop_duplicates("district").to_crs(epsg=4326)
seoul_ge= pd.merge(seoul_ge,df_district_ratio,how="left",left_on="district",right_on=df_district_ratio.index)

gdf_map_centroid= seoul_ge.copy()
gdf_map_centroid["geometry"]= gdf_map_centroid["geometry"].centroid

# ===============================
# Rental Volumes in five groups

gdf_map_centroid[["district","rental_vol"]].sort_values("rental_vol",ascending=False)
# district	rental_vol
# 9	강서구	    43464
# 6	영등포구	34144
# 11 마포구	    21643
# 8	구로구	    21501
# 1	송파구	    20544
# 4	관악구	    18090
# 2	강남구	    17221
# 13 은평구	    13144
# 19 동대문구	10346

import geoplot as gplt 
import geoplot.crs as gcrs
import mapclassify as mc
import pyproj
plt.style.use("fivethirtyeight")
plt.style.use("seaborn-notebook")

q5= mc.Quantiles(gdf_map_centroid["rental_vol"],k=5) # Rental Volumes in five groups
# q7_arr= np.array([q7.adcm])

seoul_ge["quantiles"]= q5

plt.style.use("seaborn-notebook")
plt.style.use("bmh")

font_path= r"C:\Windows\Fonts\SourceCodePro-Black.ttf".replace("\\","/")

font_name= font_manager.FontProperties(fname=font_path).get_name()

rc("font",family=font_name)

fix,ax= plt.subplots(1,figsize=(18,12))
ax= seoul_ge.plot(ax=ax,column="rental_vol",zorder=-1,linewidth=1,scheme="quantiles",legend=True,legend_kwds={"fmt":"{:.0f}","loc":"upper left"},cmap="plasma_r",edgecolor="lightskyblue")#,figsize=(18,12)

# proj= gcrs.WebMercator()
# gplt.polyplot(gdf_map_ge,zorder=-1,linewidth=1,projection=proj,facecolor="lightgray",edgecolor="white",figsize=(15,10))

# gplt.pointplot(gdf_map_centroid,projection=proj,scale="rental_vol",limits=(20,80),hue="rental_vol",scheme=q7,cmap="viridis_r",legend=True,legend_var="hue",ax=ax)

# plt.setp(ax.get_legend().get_texts(), fontsize='16')
ax.set_axis_off()
plt.setp(ax.get_legend().get_texts(), fontsize='22')
plt.axis("equal")
plt.title("Rental Volume per District in 5 Groups, 2011–2020",fontsize=26,pad=40)
plt.show()


# PLOT
#
# Rental Units, Street Demarcation
import matplotlib

# Medium, Semibold, Bold, Black
font_path= r"C:\Windows\Fonts\SourceCodePro-Black.ttf".replace("\\","/")

font_name= matplotlib.font_manager.FontProperties(fname=font_path).get_name() # D2Coding

matplotlib.rc("font",family=font_name)
# 

import matplotlib.pyplot as plt
import contextily as ctx
import geoplot as gplt 
import geoplot.crs as gcrs
# ========================
# ADD BACKGROUND MAP
seoul_strt_ge= gdf_seoul_strt.drop_duplicates("str_code").to_crs(epsg=4326) # google earth
extent= seoul_strt_ge.total_bounds
extent

proj= gcrs.WebMercator()
plt.figure(figsize=(25,20))
# fig,ax= plt.subplots(figsize=(18,13),subplot_kw='projection': proj})
ax = plt.axes(projection=proj)
ax.set_extent(extent)

# seoul_strt_ge.plot("street")
ax = gplt.polyplot(
    seoul_strt_ge,
    facecolor='coral',
    edgecolor="coral",
    alpha=.5,
    linewidth=4,
    projection=proj,
    ax=ax
)

gplt.webmap(seoul_strt_ge,ax=ax,provider=ctx.providers.Stamen.TonerLite)

plt.title("Streets of the Rental Units",fontsize=32)
plt.savefig("Streets of the Rental Units_google_earth.png")
plt.show()

# =============================
# DATA DISTRIBUTION

# gdf_seoul_dist.columns
cols=['unit_size', 'deposit', 'pay_monthly', 'floor',
       'yr_built']

gdf_seoul_dist[cols].hist(bins=50,figsize=(10,8))
plt.title("Data Distribution by Feature",fontsize=18)
plt.savefig("02_histogram_5_features.png")
plt.tight_layout()
plt.show()

# EDA
# Correlation among features
df_mon.dtypes
import seaborn as sns
corr_mon= df_mon.drop("id",axis=1).corr()
plt.figure(figsize=(7,6))
mask= np.triu(np.ones_like(corr_mon))
grid= sns.heatmap(corr_mon,mask=mask, cbar=True, square= False, fmt='.1f',\
            annot=True, annot_kws={'size':12}, cmap='winter_r')
grid.set_xticklabels(grid.get_xticklabels(), rotation = 30, fontsize = 11)
plt.title("Correlation Between the Features",fontsize=15,pad=5)
plt.savefig("step2_10_df_mon.corr().png")
plt.show()

# ===================================
# FEATURE ENGINEERING
#
# Transform skewed data

from scipy.stats import shapiro 
columns= ["district","rent_type","unit_size","deposit","pay_monthly","floor","yr_built"]
for col in columns[1:]:
  print(col,shapiro(gdf_seoul_dist[col])[1],"less than 0.05?",\
        shapiro(gdf_seoul_dist[col])[1]<.05)

# using pandas.DataFrame.skew()
#
# calculate skew and sort
skew_feats= gdf_seoul_dist[columns].skew().sort_values(ascending=False)
skewness= pd.DataFrame({"Skew":skew_feats})
skewness

# PLOT

import warnings
warnings.filterwarnings("ignore")

col_desc_en= ["Unit Size (m²)",\
           "Deposit (₩10K)",\
           "Rent (₩10K)",\
           "Year Built",\
           "Floor"] 
col_desc_ko= ["전용면적 (m²)",
           "보증금 (만원)",\
           "월세 (만원)",\
           "건축년도",\
           "입주층"]
colors = [
    "blue",
    "orange",
    "green",
    "red",
    "purple",
    "brown",
    "coral",
    "gray",
    "olive",
    "turquoise",
]

plt.style.use("seaborn-notebook")
fig,ax= plt.subplots(nrows=5,ncols=3,figsize=(12,15),\
                     edgecolor="k")
fig.subplots_adjust(top=.3)  # get the font based on the font_path

for i in range(len(columns[1:])): # exclude rent_type
  col= columns[i]
  color= colors[i%len(colors)]
  for j in range(3):
    sqrt_feat= df_mon[col]**(.5)
    sns.distplot(sqrt_feat,ax=ax[i,0],color=color,hist_kws=dict(alpha=.2),\
                 ).set_title("square-root transform - {}".format(col))

    recip_feat= 1/df_mon[col]
    sns.distplot(recip_feat,ax=ax[i,1],color=color,hist_kws=dict(alpha=.2),\
                 ).set_title("reciprocal transform - {}".format(col))

    log_feat= np.log(df_mon[col])
    sns.distplot(log_feat,ax=ax[i,2],color=color,hist_kws=dict(alpha=.2),\
                 ).set_title("log transform - {}".format(col))

  fig.suptitle("Data Transformation (Rent Type: Monthly Payment)",y=1.01,fontsize=18)
plt.tight_layout()
plt.show()

# Transformation methods
# 1. square-root
# 2. reciprocal
# 3. log 
#
# unit_size: reciprocal
# deposit: sqrt
# pay_monthly: sqrt
# floor: sqrt
# yr_built: sqrt

cols_mon= ["id","district", "rent_type","unit_size","sign_date","deposit","pay_monthly","floor","yr_built","geometry"]
df_mon= gdf_seoul_dist[cols_mon]

df_mon.unit_size= 1/df_mon["unit_size"] # reciprocal
df_mon.deposit= df_mon["deposit"]**(.5) # square-root
df_mon.pay_monthly= df_mon["pay_monthly"]**(.5)
df_mon.floor= df_mon["floor"]**(.5)
df_mon.yr_built= df_mon["yr_built"]**(.5)


# =================================================
"""### CREATE TEST AND VALIDATION SETS"""

import numpy as np

# mask_mon= np.random.rand(len(df_mon)) < .8
# train_mon= df_mon[mask_mon]
# val_mon= df_mon[~mask_mon]

# print('Training data set length='+str(len(train_mon)))
# print('Validation data set length='+str(len(val_mon)))
# print("")

# create test and test sets
train= df_mon[df_mon.sign_date.dt.year<2021]
test= df_mon[df_mon.sign_date.dt.year>2020]
train.shape, test.shape
print('Training data set length='+str(len(train)))
print("")
print('Validation data set length='+str(len(test)))
# Training data set length=284785
# Validation data set length=29844


"""## Spatial Regression"""

# !pip install pysal

from pysal.model import spreg

train_cols= ["unit_size","deposit","floor","yr_built"]

model_base= spreg.OLS(train[["pay_monthly"]].values,train[train_cols].values,name_y="pay_monthly", name_x=train_cols)
print(model_base.summary)

# save summary to file
with open("model_base.spreg.OLS.summary.txt","w") as f:
  f.write(model_base.summary)

"""### Regression Summary

- Coefficients:  the estimates for $\beta_k$ in our model. In other words, these numbers express the relationship between each explanatory variable and the dependent one, once the effect of confounding factors has been accounted for. 
"""


# =====================================================
# The model might display some clustering in errors. To interrogate this, we can do a few things.
# 
# One simple concept might be to look at the correlation between the error in predicting a site's pay_monthly and the error in predicting its nearest neighbor.
# 
# To examine this, we first might want to split our data up by rent_type and see if we’ve got some spatial structure in our residuals.
# 
# Our model does not include any information about rent_type, a key aspect that determines a monthly payment.
# 
# Therefore, we might want to see whether or not our errors are higher or lower depending on whether or not a site is rented for a lump-sum payment or not:
df_mon.rent_type.astype(bool)

is_monthly= train["rent_type"].astype(bool)
monthly= model_base.u[is_monthly]
not_monthly=model_base.u[~is_monthly]


import matplotlib.pyplot as plt

plt.style.use("bmh")
plt.style.use("seaborn-notebook")
plt.figure(figsize=(6,5))
plt.hist(monthly,density=True,label="Monthly")
plt.hist(not_monthly,histtype="step",density=True,\
         linewidth=3,label="Lump-Sum")
plt.vlines(0,0,.165,linestyle=":",color="k",linewidth=3)
plt.legend()
plt.savefig("spreg.OLS.residuals_by_rent_type.png")
plt.show()


# The average errors are similar but the variance for the lump-sum type is greater.

# A $t$ test shows the two distributions are distinct from one another.

import scipy.stats as stats
stats.ttest_ind(monthly,not_monthly)
# Ttest_indResult(statistic=array([-306.24088061]), pvalue=array([0.]))

"""Calculate the T-test for the means of two independent samples of scores.

This is a two-sided test for the null hypothesis that 2 independent samples have identical average (expected) values. This test assumes that the populations have identical variances by default.

A t-value of 0 indicates that the sample results exactly equal the null hypothesis. As the difference between the sample data and the null hypothesis increases, the absolute value of the t-value increases.
"""

# ==================================================
"""### Distribution of residuals in each district"""

train.district.unique().tolist()
dist_en= ['Gang-nam',
 'Gang-dong',
 'Gang-buk',
 'Gang-seo',
 "Gwan-ak",
 'Gwang-jin',
 'Guro',
 'Geum-cheon',
 'Nowon',
 'Dobong',
 'Dong-daemun',
 'Dong-jak',
 'Mapo',
 'Seo-daemun',
 'Seo-cho',
 'Seong-dong',
 'Seong-buk',
 'Song-pa',
 'Yang-cheon',
 'Young-deungpo',
 'Yongsan',
 'Eun-pyeong',
 'Jong-no',
 'Jung-gu',
 'Jung-nang']

"""1. Sort the data by the median residual in that district,
2. Make a box plot, which shows the distribution of residuals in each district:
"""

train["residual"]= model_base.u
medians= train.groupby(
    "district"
).residual.median().to_frame("district_residual")

# the location of the font file
# my_font = fm.FontProperties(fname=font_path)  # get the font based on the font_path

# ax.set_xlabel(u'Some text', fontproperties=my_font)
# ax.set_ylabel(u'Some text', fontproperties=my_font)
# ax.set_title(u'title', fontproperties=my_font)


import seaborn as sns
# plt.style.use("bmh")
fig= plt.figure(figsize=(15,10))
ax= plt.gca()
sns.boxplot("district","residual",ax=ax,data=\
            train.merge(medians,how="left",\
                         left_on="district",right_index=True
                         ).sort_values("district_residual"),\
            palette="bwr")
ax.set_xticklabels(dist_en,fontsize=14)#,              fontproperties=custom_font
ax.set_ylabel("Residual",fontsize=16)
ax.set_xlabel("District",fontsize=16)
fig.autofmt_xdate()
plt.title(" Distribution of Residuals in Each District",fontsize=20)
plt.savefig("residuals_distribution_per_district.png")
plt.show()

"""- No district is disjoint from one another, but some are higher than others,
- e.g. 강남구, 용산구, 종로구, 중구
- There may be a distinctive effect of district foot-traffic that matters in this model.

<br>

---
<br>

The relationship between an observation's residuals and its surrounding residuals.

- Use spatial weights to represent the geographic relationships between observations.
"""



# Spatial Heterogeneity
#  At its most basic, spatial heterogeneity means that parts of the model may change in different places. For example, changes to the intercept, α, may reflect the fact that different areas have different baseline exposures to a given process. Changes to the slope terms, β, may indicate some kind of geographical mediating factor, such as when a governmental policy is not consistently applied across jurisdictions. Finally, changes to the variance of the residuals, commonly denoted σ2, can introduce spatial heteroskedasticity. We deal with the first two in this section.
# ...
# For example, let us include a binary variable for every neighborhood, indicating whether a given house is located within such area (1) or not (0). Mathematically, we are now fitting the following equation:
# 
# $\log{P_i} = \alpha_r + \sum_k \mathbf{X}_{ik}\beta_k  + \epsilon_i$
#
# where the main difference is that we are now allowing the constant term, α, to vary by district r, α_r.

# equation

features= ['unit_size', 'deposit','floor', 'yr_built']
f= "pay_monthly ~ " + " + ".join(features) + " + district - 1"
# 'pay_monthly ~ unit_size + deposit + floor + yr_built + district - 1'

# Critically, note that the trailing -1 term means that we are fitting this model without an intercept term. This is necessary, since including an intercept term alongside unique means for every district would make the underlying system of equations underspecified.

import statsmodels.formula.api as sm
model_sm_ols= sm.ols(f,data=train).fit()
print(model_sm_ols.summary2())


# The approach above shows how spatial FE (fixed effects) are a particular case of a linear regression with a categorical variable. District membership is modeled using binary dummy variables. 

# save to file
with open("model_fe_district.sm.ols.txt","w") as f:
  output= model_sm_ols.summary2().as_text()
  f.write(output)

# PySAL Regimes functionality
# which allows the user to specify which variables are to be estimated separately for each “regime”. In this case however, instead of describing the model in a formula, we need to pass each element of the model as separate arguments.

model_spreg= spreg.OLS_Regimes(
  train[["pay_monthly"]].values,
  train[features].values,
  train.district.tolist(),
  constant_regi="many",
  cols2regi=[False]*len(features),regime_err_sep=False,
  name_y="pay_monthly",
  name_x=features)

print(model_spreg.summary)

# save to file
with open("model_fe_district.spreg.OLS_summary.txt","w") as f:
  f.write(model_spreg.summary)

  
# Econometrically speaking, instead of comparing all rent prices across the city as equal, we only derive variation from within each postcode.
# 
# Remember that the interpretation of β_k is the effect of variable k, given all the other explanatory variables included remain constant.
# 
# By including a single variable for each area, we are effectively forcing the model to compare as equal only rent prices that share the same value for each variable; or, in other words, only sites located within the same area.
# 
# Introducing FE affords a higher degree of isolation of the effects of the variables we introduce in the model because we can control for unobserved effects that align spatially with the distribution of the FE introduced (by postcode, in this case).

# ==============
# Fixed Effects
#
# https://statisticsbyjim.com/regression/interpret-coefficients-p-values-regression/
#
# Fixed effects are variables that are constant across individuals; these variables, like age, sex, or ethnicity, don’t change or change at a constant rate over time. They have fixed effects; in other words, any change they cause to an individual is the same. For example, any effects from being a woman, a person of color, or a 17-year-old will not change over time.
#
# For purposes of research and experimental design, these variables are treated as a constant.


# ======================================
# PLOT 
# map of district fixed effects
#
# 1. EXTRACT ONLY THE EFFECTS PERTAINING 
# to the districts
#
# ui=μi–μ : pay_monthly_i - pay_monthly_mean (residuals)

district_effects= model_sm_ols.params.filter(like="district")
district_effects.head()
# district[강남구]   -437.263650
# district[강동구]   -438.881841
# district[강북구]   -440.076605
# district[강서구]   -439.087872
# district[관악구]   -437.735622
# dtype: float64

# 2. EXTRACT JUST THE DISTRICT NAME FROM THE INDEX OF THE SERIES
stripped= district_effects.index.str.strip("district[").str.strip("]")
district_effects.index= stripped
district_effects= district_effects.to_frame("fixed_effect")
district_effects.head()
# 	fixed_effect
# 강남구	-437.263650
# 강동구	-438.881841
# 강북구	-440.076605
# 강서구	-439.087872
# 관악구	-437.735622

# 3. JOIN THE DISTRICT NAMES WITH THE DISTRICT SHAPES
seoul_dists.columns= ['dist_code', 'district', 'SGG_OID', 'COL_ADM_SE', 'GID', 'geometry']


fix,ax= plt.subplots(figsize=(15,10))
seoul_dists.plot(color="gray",alpha=.5,ax=ax)
seoul_dists.merge(
  district_effects,
  how="left",
  left_on="district",
  right_index=True
  ).dropna(subset=["fixed_effect"]
  ).plot(
    "fixed_effect",ax=ax,edgecolor="gray",cmap="viridis",legend=True
    )
ax.set_title("District Fixed Effects (District Coefficients)",fontsize=20)
plt.savefig("08_seoul_district_fixed_effects.png")
plt.show()


# P-values and coefficients in regression analysis work together to tell you which relationships in your model are statistically significant and the nature of those relationships. The coefficients describe the mathematical relationship between each independent variable and the dependent variable. The p-values for the coefficients indicate whether these relationships are statistically significant.


# ===============================
# PREDICTION AND EVALUATION
# predict validation set
y_true= test["pay_monthly"]
y_pred= model_sm_ols.predict(test)

# reverse-transform from square-root
y_true= y_true**2
y_pred= y_pred**2

# if y_pred is less than zero, make it zero
y_pred_adj= y_pred.apply(lambda x: 0 if x < 0 else x)


# =====================================
# REGRESSION METRICS
# 
# R²
# The coefficient of determination is a measure of how well future samples will be predicted by the model. The best possible score is 1.

# MSE, Mean Squared Error
# MSE = 1 / N * sum for i to N (y_i – yhat_i)^2
# 
import sklearn.metrics as metrics

def print_evaluate(true, predicted):  
    mae = metrics.mean_absolute_error(true, predicted)
    mse = metrics.mean_squared_error(true, predicted)
    rmse = np.sqrt(metrics.mean_squared_error(true, predicted))

    # R² (coefficient of determination) regression score function. Best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse). A constant model that always predicts the expected value of y, disregarding the input features, would get a R² score of 0.0.
    r2_score = metrics.r2_score(true, predicted)
    print('==================================')
    print("  Regression Evaluation Metrics")
    print('==================================')
    print('Mean Absolute Error:       ', round(mae,2))
    print("")
    print('Mean Squared Error:      ', round(mse,2))
    print("")
    print('Root Mean Square Error:   ', round(rmse,2))
    print("")
    print('R2 Score:                  ', round(r2_score,2))

# MAE: 8.97
# is the easiest to understand, because it's the average error.
#
# MSE:  339.86
# is more popular than MAE, because MSE "punishes" larger errors, which tends to be useful in the real world.
#
# RMSE: 18.44
# is even more popular than MSE, because RMSE is interpretable in the "y" units.
#
# All of these are loss functions, because we want to minimize them.

print_evaluate(y_true, y_pred_adj)

# ===================
# REGRESSION PLOT
plt.hist(y_true,y_pred_adj)
plt.plot(y_pred_adj,"r")

# ===================
# Residual Histogram
#
# can be used to check whether the variance is normally distributed. A symmetric bell-shaped histogram which is evenly distributed around zero indicates that the normality assumption is likely to be true.
import seaborn as sns
# plt.style.use("seaborn-notebook")
plt.style.use("bmh")
plt.figure(figsize=(4,8))
sns.displot((y_true - y_pred_adj), bins=2)
plt.title("Residuals (y_true - y_pred)",fontsize=16)
plt.savefig("09_residuals_true_vs_pred.png")
plt.show()