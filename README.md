<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="generator" content="pandoc">
  <meta name="author" content="Jieun K">
  <meta name="dcterms.date" content="2021-07-17">
  <!--<title>Data Analytics in Practice</title> -->
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, minimal-ui">
  <link rel="stylesheet" href="./revealjs/dist/reset.css">
  <link rel="stylesheet" href="./revealjs/dist/reveal.css">
  <link rel="stylesheet" href="./revealjs/dist/theme/black.css" id="theme">
</head>
<body>
  <div class="reveal">
    <div class="slides">      
      <section id="title-slide">
        <h1 class="title"><span style="color: lightseagreen;">Data Analytics</span> in Practice</h1>
        <h3><p class="subtitle"><span style="color: gold;">Couse Project</span></p></h3>        
        <p class="author">Jieun K</p>
        <p class="date">August 4, 2021</p>
      </section>
      <!-- SLIDE: Subtitle -->
      <section id="eda-feature-engineering-and-regression-modelling-with-real-estate-data" class="title-slide slide level1">
        <h2><span style="color: lightgreen;">EDA</span>, <span style="color: lightpink;">Feature Engineering</span> , and <span style="color: lightskyblue;">Regression Modelling</span> with <span style="color: burlywood;">Real Estate Data</span> </h2>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: abstract -->      
      <section class="slide level1">
        <section id="abstract-what-is-the-project-about" class="title-slide slide level2">
          <h3>What is the <span style="color: lightskyblue;">project</span> about ❓</h3>
        </section>  
        <section class="slide level2">    
        <p>Practice data science with real-estate data</p>
        </section>
        <section class="slide level2">      
        <p>Demonstrate a commonly used pipeline ➡️</p>
        </section>
        <section class="slide level2">      
        <p>Preprocessing ⇒ <span style="color: gainsboro;">
         EDA </span> ⇒ <span style="color: gainsboro;">Feature Engineering</span> ⇔ Modelling ⇒ Performance Evaluation</p>
        </section>        
        <!-- 
        <section id="pose-a-question" class="slide level2">
          <h4>Fit a Model</h4>
          <ul>
          <li>Build a regression <span style="color: lightseagreen;">model</span></li>
          <li>Do <span style="color: lightpink;">feature engineering</span>  if possible</li>
          </ul>
        </section>
        <section id="and-answer" class="slide level2">
          <h4>Predict and Evaluate</h4>
          <li><span style="color: lightsalmon;">Predict</span> monthly rent based on historical data</li>
          <li>Gauage <span style="color: lightskyblue;">performance</span> with <span style="color: lightpink;">evaluation metrics</span</li>
        </section> -->
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: sections -->
      <section class="slide level1">
        <section id="sections" class="title-slide slide level2">          
          <h2>Sections</h2>
        </section>
        <section class="slide level2">    
          <ul>
          <li>Introduction</li>
          <li>Dataset</li>
          <li>Pre-processing</li>
          <li>EDA</li>
          <li>Feature Engineering</li>
          <li>Model Fitting</li>
          <li>Prediction and Evaluation</li>
          <!-- <li>Conclusion</li> -->
          </ul>
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: introduction -->
      <section class="slide level1">
        <section id="introduction" class="title-slide slide level2">          
          <h2>Introduction</h2>
        </section>
        <section id="introduction-1" class="slide level2">
          <h3>Introduction</h3>
          <ol type="1">
          <li><p>What is an officetel❓</p></li>
          <li><p><span style="color: lightslategrey;"></span>A growing portion of the housing market</p></li>
          <li><p>Did Covid-19 change anything❓</p></li>
          <li><p>Objectives of the project</p></li>
          </ol>
        </section>
      </section>
      <!-- SLIDE: intro-definition -->           
      <section class="slide level1">
        <section id="what-is-an-officetel" class="title-slide slide level2">
          <h3>1. What is an officetel?</h3>
        </section>
        <section class="slide level2">
          <img src="./img/intro_officetel_example.jpg" alt="office building on one side of the street"/>
          <p>A building with both residential and commercial units</p>          
        </section>
        <section class="slide level2">
          A combination of <span style="color: lightseagreen;"><em>office</em></span> and <em><span style="color: lightsalmon;">hotel</span></em>
        </section>        
        <section class="slide level2">
          Offers convenience through <span style="color: palevioletred;">amenities</span> inside or around the property
        </section>        
        <section class="slide level2">
          <span style="color: salmon;">Amenities: </span><br> <span style="color: lightgoldenrodyellow;">|</span>
          dry-cleaning &amp; laundry services 🧼 <span style="color: lightgoldenrodyellow;">|</span><br>
           <span style="color: lightgoldenrodyellow;">|</span> gyms 💪 
           <span style="color: lightgoldenrodyellow;">|</span> restaurants 🥘 <span style="color: lightgoldenrodyellow;">|</span><br>
            <span style="color: lightgoldenrodyellow;">|</span> hair salons ✂️ <span style="color: lightgoldenrodyellow;">|</span> shops 🛍️ <span style="color: lightgoldenrodyellow;">|</span>  
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: introduction -->
      <section class="slide level1">
        <section id="introduction-1" class="slide level2">
          <h3>Introduction</h3>
          <ol type="1">
          <li><p>What is an officetel❓</p></li>
          <li><p><span style="color: lightskyblue;"> A growing portion of the housing market</span></p></li>
          <li><p>Did Covid-19 change anything❓</p></li>
          <li><p>Objectives of the project</p></li>
          </ol>
        </section>
      </section>
      <!-- SLIDE: intro-growing share -->           
      <section class="slide level1">        
        <section id="officetels-a-growing-share-of-housing-market" class="title-slide slide level2">
          <h3>2. Officetels: A growing share of housing market</h3>
        </section>
        <section class="slide level2">    
          <ul>
          <li><p>Biggest supply in Seoul Metropolitan Area</p></li>
          <li><p>In <span style="color: lightseagreen;">city centers</span> and areas of <span style="color: lightsalmon;">high-mobility</span></p></li>
          </ul>
        </section>          
        <section class="slide level2">    
          <ul>
          <li><p> Demand from <span style="color: palevioletred;">one-person</span> households on the rise</p></li>
          <li><p> 14% jump from 2015 to 2018 at <span style="color: rgb(84, 84, 185);">370,000 units</span></p></li>
          </ul>
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: introduction -->
      <section class="slide level1">
        <section id="introduction-1" class="slide level2">
          <h3>Introduction</h3>
          <ol type="1">
          <li><p>What is an officetel❓</p></li>
          <li><p>A growing portion of the housing market</p></li>
          <li><p><span style="color: lightskyblue;">Did Covid-19 change anything❓</span> </p></li>
          <li><p>Steps of the project</p></li>
          </ol>
        </section>
      </section>
      <!-- SLIDE: intro-Did Covid-19 change anything? -->        
      <section class="slide level1">
        <section id="did-covid-19-change-anything" class="title-slide slide level2">
          <h3>3. Did Covid-19 change anything❓</h3>
        </section>
        <section class="slide level2">   
          Property <span style="color: lightseagreen;">sales</span> in 1st quarter of 2020 <span style="color: lightsalmon;">increased</span>
        </section>          
        <section class="slide level2"> 
          61.1% (<span style="color: rgb(45, 168, 45);">Seoul</span>) and 52.8% (<span style="color: greenyellow;">Incheon</span>) ⬆️ from previous year
        </section>        
        <section class="slide level2">
          <span style="color: plum;">Rental</span> volume <span style="color: rgb(129, 170, 68);">steady</span> for the foreseeable future
        </section>          
        <section class="slide level2">    
          <ul>
          <li><p>Property sales on the upward trend</p> </li>
          <li><p>among investors looking for stable income</p> </li>
          </ul>
        </section>          
        <section class="slide level2">    
          <ul>
          <li><p>More construction of <span style="color: lightsalmon;">20m²–40m²</span> units</p></li>
          <li><p>These units to occupy <span style="color: lightseagreen;">64%</span> of the total rentals in <span style="color: lightskyblue;">2022</span></p></li>
          </ul>
        </section>            
        <section class="slide level2">  
          <a href="https://www.kbfg.com/kbresearch/report/reportView.do?reportId=2000121">Data by KB Financial Group (July 16, 2020)</a>
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: introduction -->
      <section class="slide level1">
        <section id="introduction-1" class="slide level2">
          <h3>Introduction</h3>
          <ol type="1">
          <li><p>What is an officetel❓</p></li>
          <li><p>A growing portion of the housing market</p></li>
          <li><p>Did Covid-19 change anything❓</p></li>
          <li><p><span style="color: lightskyblue;">Steps of the project</span></p></li>
          </ol>
        </section>
      </section>
      <!-- SLIDE: intro-Objectives -->
      <section class="slide level1">          
        <section id="objectives-of-this-project" class="title-slide slide level2">
          <h3>4. Steps of the project</h3>
        </section>
        <section class="slide level3">
          <h3>Step 1: Pre-Processing </h3>
          <ul>            
          <li>Cleaning</li>
          <li>Data <span style="color: lightseagreen;">Imputation</span></li>
          </ul>
        </section>
        <section class="slide level3"> 
          <h3>Step 2: EDA </h3>
          <ul>
          <li>Statistics <span style="color: lightseagreen;">by district</span></li>
          <li>Rental <span style="color: plum;">volume</span></li>
          <li>Rental type <span style="color: lightsalmon;">ratio</span> </li>
          <li>Unit size, etc.</li>
          <li>Correlation between key features</li>
          </ul>
        </section>
        <section class="slide level3">
          <h3>Step 3: Feature Engineering </h3>
          <ul>            
          <li> Add <span style="color: lightsalmon;">geometry</span> to <span style="color: lightseagreen;"> <code>district</code></span> and <span style="color: plum;"> <code>street</code> </span></li>
          <li>Visualize data on a map</li>
          <li> <span style="color: lightskyblue;">Transform</span> skewed data</li>
          </ul>
        </section>
        <section class="slide level3">
          <h3>Step 4: Model Fitting </h3>
          <ol>    
            <li>Baseline model: <br>
               <span style="color: lightpink;"> <code>rent</code> </span> <span style="color: red;">~</span> 
              <span style="color: lightseagreen;"> <code>unit_size</code> </span> <span style="color: white;">+</span> <span style="color: lightseagreen;"> <code>deposit</code>  </span> <span style="color: white;">+</span> <span style="color: lightseagreen;"> <code>floor</code> </span> <span style="color: white;">+</span> <span style="color: lightseagreen;"> <code>yr_built</code> </span> </li>
              <hr>
            <li><span style="color: lightskyblue;">Fixed effects</span> model: <br>
               Baseline <span style="color: white;">+</span> <span style="color: gold;"> <code>district</code> </span></li>
          </ol>
        </section>
        <section class="slide level3">
          <h3>Step 5: Prediction and Evaluation</h3>
          <ul>            
          <li>Mean <span style="color: brown;">Absolute</span> Error </li>
          <li>Mean <span style="color: lightseagreen;">Squared</span> Error </li>
          <li><span style="color: plum;">Root</span> Mean Squared Error </li>
          <li><span style="color: gold;">R²</span>  Score</li>
          </ul>
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: dataset -->
      <section class="slide level1">
        <!-- <section id="dataset" class="title-slide slide level2">
          <h2>Dataset</h2>
        </section> -->
        <section id="dataset-1" class="slide level2">
          <h3>Dataset</h3>
          <ul>
          <li>Seoul Officetel rentals data from <span style="color: lightseagreen;">2011-2021</span></li>
          <li>Download available (per 365-day period)</li>
          <li>Open Data Portal (<a href="https://www.data.go.kr">공공데이터포털</a>)</li>
          </ul>
          <aside class="notes">
          📝 The maximum time period of the file is a year for the whole city of Seoul
          </aside>
        </section>        
        <section class="slide level2">    
          <ul>
          <li>🇰🇷 <a href="https://www.data.go.kr/data/3050988/fileData.do">서울 오피스텔 전월세 거래 데이터</a></li>
          <li>Dataset (2011–2021): <span style="color: lightsalmon;">314,629</span> rows, <span style="color: lightseagreen;">14</span> columns</li>
          </ul>
        </section>        
        <section class="slide level2">    
          <ul>
          <li>시군구 | 번지 | 본번 | 부번 | 단지명 | 도로명</li>
          <li>전월세구분 | 전용면적(㎡) | 층 | 건축년도</li>
          <li>계약년월 | 계약일</li>
          <li>보증금(만원) | 월세(만원)</li>
          </ul>
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: pre-processing -->
      <section class="slide level1">
        <section id="pre-processing" class="title-slide slide level2">
          <h2>1. Pre-Processing</h2>        	
        </section>
        <section class="slide level2">
          <img src="./img/1.1_data_description.png" alt="Data description is automatically added to the file when downloading"/>
          <p>Description automatically added to file when downloading</p>
        </section>        
        <section class="slide level2">    
          <ul>
          <li><p>Needs removal before <code>pandas.read_csv()</code></p></li>
          <li><p>Done manually ✔️ (or programmatically)</p></li>
          </ul>
        </section>        
        <section class="slide level2">    
          <img src="./img/1.2_csv_2014.jpg" alt="The csv file for the year 2014 is untidy" height="400"/>  
          <p>                  
          <ul>
          <li>2014 file is “untidy”</li>
          <li>Needs cleanup
          </li>
          </ul>
          </p>  
        </section>        
        <section class="slide level2">    
          <p>Merge 10 datasets into one <code>pandas.DataFrame</code></p>
          <p><img src="./img/1.3_merge_dataframe.jpg" alt="Merge 10 datasets into one `pandas.DataFrame`" height="500"/></p>
        </section>        
        <section class="slide level2">
          <h4>Fill in <span style="color: lightskyblue;">street addresses</span> </h4>
          <ul>
          <li>Search and replace</p></li>
          <li><p>Done manually ✔️</p></li>
          </ul>
        </section>
        <section class="slide level2">
          <h4>Fill in <span style="color: lightskyblue;">`year built`</span> </h4>
          <ul>
          <li>with the district <span style="color: lightsalmon;">median</span></li>
          </ul>
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: 2. EDA -->
      <section class="slide level1">
        <section id="eda" class="title-slide slide level2">
          <h2>2. EDA</h2>
          <ul>
            <li>Yearly Rental Volume</li>
            <li> <span style="color: lightskyblue;">Yearly Rental Volume by Type</span> </li>
            <li>Stats by District</li>
            <li> <span style="color: lightskyblue;">Data Distribution by Key Feature</span> </li>
            <li>Correlation Between Features</li>
          </ul>   	
        </section>
        <section class="slide level2">
          <img src="./img/step2_01_yearly_rental_vol.png" alt="Yearly Rental Volume"/>
          <p>Rentals steadily increasing (2021 data as of July 31)</p>          
        </section>
        <section class="slide level2">
          <img src="./img/step2_02_yearly_rental_vol_by_rent_type.png" alt="Yearly Rental Volume by Type"/>
          <p>Covid-19 impact on the rental volume? None? </p>          
        </section>
        <section class="slide level2">
          <img src="./img/step2_03_stats_by_district_1_unit_size.png" height="500" alt="Unit Size (m²) by District"/>
          <p>Unit Size (m²) by District</p>          
        </section>
        <section class="slide level2">
          <img src="./img/step2_04_stats_by_district_rent_type_ratio.png" height="500" alt="Rent Type Ratio by District"/>
          <p>Rent Type Ratio by District</p>          
        </section>        
        <section class="slide level2">
          <img src="./img/step2_05_stats_by_district_deposit.png" height="500" alt="Deposit (in ₩10K) by District"/>
          <p>Deposit (in ₩10K) by District</p>    
        </section>        
        <section class="slide level2">
          <img src="./img/step2_06_stats_by_district_rent.png" height="500" alt="Monthly Rent (in ₩10K) by District"/>
          <p>Monthly Rent (in ₩10K) by District</p>    
        </section>        
        <section class="slide level2">
          <img src="./img/step2_07_stats_by_district_yr_built.png" height="500" alt="Year Built by District"/>
          <p>Year Built by District</p>    
        </section>        
        <section class="slide level2">
          <img src="./img/step2_08_stats_by_district_floor.png" height="500" alt="Unit Floor by District"/>
          <p>Unit Floor by District</p>    
        </section>        
        <section class="slide level2">
          <img src="./img/step2_09_histogram_five_features.png" height="500" alt="Data Distribution by Key Feature"/>
          <p>Data distribution → transformation necessary</p>
        </section>        
        <section class="slide level2">
          <img src="./img/step2_10_df_mon.corr().png" alt="Data Distribution by Key Feature"/>
          <div>Feature Correlation</div>
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: Feature Engineering -->
      <section class="slide level1">
        <section id="feature-engineering" class="title-slide slide level2">
          <h2>3. Feature Engineering</h2>
          <ul>            
            <li> Add <span style="color: lightsalmon;">geometry</span> to <span style="color: lightseagreen;"> <code>district</code></span> and <span style="color: plum;"> <code>street</code> </span></li>
            <li>Visualize data on a map</li>
            <li><span style="color: lightskyblue;">Transform</span> features</li>
            </ul>	
        </section>
        <section class="slide level2">
          <h4>Add <span style="color: lightpink;">Geometry</span> </h4>
          <ul>
          <li>Shape files (.shp):
            <ul>
              <li><a href="http://data.nsdi.go.kr/dataset/15144">서울 행정구역시군구_경계</a> (국가공간정보포털)</li>
              <li><a href="http://http://data.nsdi.go.kr/dataset/12902">서울 도로명주소 도로구간</a> (국가공간정보포털)</li>
            </ul>
          </li>
          <li>
            Visualize with <span style="color: lightseagreen;"> <code>geopandas</code> </span> and <span style="color: lightseagreen;"> <code>geoplot</code> </span> 
          </li>
          </ul>
        </section>        
        <section class="slide level2">
          <img src="./img/step3_01_rental_volumes in five groups_with_labels.png" height="500" alt="Data Distribution by Key Feature"/>
          <p>Rental Volumes in Five Groups</p>
        </section>        
        <section class="slide level2">
          <img src="./img/step3_02_rental units_street_demarcation.png" alt="Rental Units - Streets"/>
          <p>Rental Units: Street Demarcation | 도로경계</p>
        </section>
        <section class="slide level2">
          <h4>Data <span style="color: lightpink;">Transformation</span> </h4>
          <ul>
          <li>unit_size</li>
          <li>deposit</li>
          <li>pay_monthly</li>
          <li>floor</li>
          <li>yr_built</li>
          </ul>
        </section>
        <section class="slide level2">
          <h4><span style="color: lightsalmon;">Before</span> Transformation </h4>
          <img src="./img/step2_09_histogram_five_features.png" height="550" alt="data distribution"/>
        </section>
        <section class="slide level2">
          <!-- <h4><span style="color: turquoise;">Transformation</span>  </h4> -->
          <img src="./img/step3_03_data_transformation.png" height="550" alt="data transformation"/>
          <p>Methods: 1. Reciprocal 2. Square root 3. Logarithm</p>
          <!-- 역수/multiplicative inverse, 제곱근,  -->
        </section>
        <section class="slide level2">
          <h4>Transformation <span style="color: lightpink;">Method</span> </h4>
          <ul>
          <li> <code>unit_size</code>: <span style="color: lightskyblue;">Reciprocal</span> </li>
          <li> <code>deposit</code>: <span style="color: lightgreen;">Square root</span> </li>
          <li> <code>pay_monthly</code>: <span style="color: lightgreen;">Square root</span> </li>
          <li> <code>floor</code>: <span style="color: lightgreen;">Square root</span> </li>
          <li> <code>yr_built</code>: <span style="color: lightgreen;">Square root</span></li>
          </ul>
        </section>
      </section> <!-- END OF FEATURE ENGINEERING -->
      <!-- ============================================================== -->
      <!-- SLIDE: 4. Modeling -->
      <section class="slide level1">
        <section id="modeling" class="title-slide slide level2">
          <h2>4. Model Fitting</h2>
          <ul>            
            <li> Train Set: <span style="color: lightsalmon;">284,284</span> rows, 2011 – 2020</li>
            <li>Test Set: <span style="color: lightskyblue;">29,611</span> rows, Jan – Jul, <span style="color: lightskyblue;">2021</span> </li>
            <hr>
            <li>Python libraries: <code>pysal</code>, <code>statsmodels</code> </li>
            <li>Baseline: <span style="color: lightpink;"> <code>rent</code> </span> <span style="color: red;">~</span> 
              <span style="color: lightseagreen;"> <code>unit_size</code> </span> <span style="color: white;">+</span> <span style="color: lightseagreen;"> <code>deposit</code>  </span> <span style="color: white;">+</span> <span style="color: lightseagreen;"> <code>floor</code> </span> <span style="color: white;">+</span> <span style="color: lightseagreen;"> <code>yr_built</code> </span> </li>
            <li>Baseline <span style="color: white;">+</span> <span style="color: gold;"> <code>district</code> </span> (<span style="color: lightyellow;">fixed effects</span>)</li>
            </ul>	
        </section>
        <section class="slide level2">
          <img src="./img/step4_01_baseline_spreg.OLS.summary_part1.png" height="560" alt="baseline regression model"/>
          <div> <span style="color: lightseagreen;">Baseline</span> model, R² score: <span style="color: lightseagreen;"> <code>0.73</code></span> </div>
        </section>
        <section class="slide level2">
          <img src="./img/step4_02_baseline_spreg.OLS.residuals_by_rent_type_2.png" height="560" alt="Residuals by rent_type"/>
          <div> Similar errors, but <span style="color: rgb(192, 69, 69);"> greater variance</span> for <span style="color: rgb(192, 69, 69);"> <code>lump-sum</code></span></div>
        </section>
        <section class="slide level2">
          <img src="./img/step4_03_t_test_distribution_of_residuals_by_rent_type.png" alt="t test score"/>
          <div> <span style="color: lightgreen;"><code>t-test</code></span> : two distributions are distinct.
          </div>
        </section>
        <section class="slide level2">
          <img src="./img/step4_04_residuals_distribution_per_district.png" alt="residuals boxplot by district"/>
          <div>Some are higher: <span style="color: rgb(85, 85, 206);">강남구</span> , <span style="color: lightpink;">용산구, 종로구, 중구</span>, etc.
          </div>
        </section>
        <section class="slide level2">
          <img src="./img/step4_05_fixed_effects_spreg.OLS_with_district_part1.png" alt="fixed effects model"/>
          <div> <span style="color: turquoise;">Fixed effects</span> model, R² score: <span style="color: turquoise;"> <code>0.76</code></span> </div>
        </section>
        <section class="slide level2">
          <img src="./img/step4_06_fixed_effects_spreg.OLS_with_district_part2.png" height="560" alt="district fixed effects"/>
          <div> <span style="color: gold;"> <code>district</code> </span> as <span style="color: turquoise;"> fixed effects </span> </div>
        </section>
        <section class="slide level2">
          <img src="./img/step4_07_seoul_district_fixed_effects.png" height="560" alt="District Fixed Effects (District Coefficients)"/>
          <div> <span style="color: gold;"> <code>district</code> </span> fixed effects</div>
        </section>
      </section> <!-- END OF Modeling -->
      <section class="slide level1">
        <section id="evaluation" class="title-slide slide level2">
          <h3>5. Prediction and Evaluation</h3>
          <ul>
            <li>Test Set: <span style="color: lightskyblue;">29,611</span> rows (<span style="color: lightskyblue;">2021</span> data)</li>
            <hr>
            <li>Regressor: 
               <span style="color: gold;">Baseline + <code>district</code> </span> (fixed effects)
            </li>
          </ul>
        </section>        
        <section id="evaluation" class="title-slide slide level2">
          <img src="./img/step5_01_histogram_residuals_true_vs_pred.png" height="560" alt="Residuals: true vs pred"/>
          <div> Residuals negatively <span style="color: lightcoral;">skewed </span></div>
        </section>        
        <section id="evaluation" class="title-slide slide level2">
          <h4>Evaluation Metrics</h4>
          <img src="./img/step5_02_regression_eval_metrics_true_minus_pred.png" alt="evaluation metrics"/>
          <div> Data size: approx. <span style="color: lightcoral;">10% of train-set </span></div>
        </section>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: to be continued -->
      <section id="end" class="title-slide slide level1">
        <h1>The End</h1>
      </section>
      <!-- ============================================================== -->
      <!-- SLIDE: thank you -->
      <section id="thank-you" class="title-slide slide level1">
        <h1>Thank You</h1>
      </section>
    </div> <!-- end of slides -->
  </div> <!-- end of reveal div -->
</body>
</html>
