@extends('layout')

<?php
	if ($scrapeinfo["boosters"])
		$boosterfromnow = round($scrapeinfo["boosters"]->fromnow/60, 0);
	
	if ($scrapeinfo["cards"])
		$cardfromnow = round($scrapeinfo["cards"]->fromnow/60, 0);
?>

@section('content')
  <div class="updated_container">
	<div class="updated_entry">
		<div class="updated_title">Boosters Updated</div>
		<div class="updated_text">{{ $boosterfromnow.' minutes ago' }}</div>
	</div>
	<div class="updated_entry">
		<div class="updated_title">Cards Updated</div>
		<div class="updated_text">{{ $cardfromnow.' minutes ago' }}</div>
	</div>
  </div>
  <div class="table_contents">
  <?php $count=0; $numads = 0; ?>
  @foreach($boosters as $booster)
    <?php $count++; ?>
    @if ($count%6 == 0 && $numads < 3)
	  <div class="table_row_ad">
		<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
		<!-- New Booster Entry -->
		<ins class="adsbygoogle"
			 style="display:inline-block;width:950px;height:76px"
			 data-ad-client="ca-pub-5367841795553109"
			 data-ad-slot="6837789070"></ins>
		<script>
		(adsbygoogle = window.adsbygoogle || []).push({});
		</script>
	   </div>
	   <?php $numads++; ?>
	@endif
    <a href="{{ $booster->booster_link }}" target="_blank"><div class="table_row_container">
      <div class="table_row_entry row_image"><img src="{{ $booster->booster_image }}"></div>
      <div class="table_row_entry row_link">{{ $booster->name }}
        <div class="row_sub">Booster Pack</div></div>
      <div class="table_row_entry price_size" style="color: {{ StyleController::getProfitColor($booster->profit) }};">
		${{ number_format($booster->profit,2) }}
        <div class="row_sub">Est. Profit</div></div>
      <div class="table_row_entry price_size">${{ number_format($booster->booster_price,2) }}
        <div class="row_sub">Booster Price</div></div>
      <div class="table_row_entry price_size" style="color: {{ StyleController::getRiskColor($booster->std_deviation) }};">${{ number_format($booster->std_deviation,2) }}
        <div class="row_sub">Risk</div></div>
      <div class="table_row_entry">
        <div class="table_row_multientry">
          <div>Highest</div>
          <div class="table_row_multientry_sub">Card</div>
          <div>Lowest</div>
        </div>
        <div class="table_row_multientry">
          <div>${{ number_format($booster->highcard_price,2) }}</div>
          <div class="table_row_multientry_sub">Price</div>
          <div>${{ number_format($booster->lowcard_price,2) }}</div>
        </div>
        <div class="table_row_multientry">
          <div>${{ number_format($booster->highcard_median,2) }}</div>
          <div class="table_row_multientry_sub">Median</div>
          <div>${{ number_format($booster->lowcard_median,2) }}</div>
        </div>
        <div class="table_row_multientry">
          <div>{{ $booster->highcard_volume }}</div>
          <div class="table_row_multientry_sub">Volume</div>
          <div>{{ $booster->lowcard_volume }}</div>
        </div>
      </div>
    </div>
    </a>
  @endforeach
  </div>
@stop