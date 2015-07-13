<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It's a breeze. Simply tell Laravel the URIs it should respond to
| and give it the Closure to execute when that URI is requested.
|
*/

Route::get('/', function()
{
  $boosters = DB::select('CALL CardHighLow(50);');
  //$boosters = BoosterProfitView::take(50)->get();
  $scrapeinfo = [ "cards" => DB::table('scrape_info')->select(DB::raw('TO_SECONDS(NOW())-TO_SECONDS(scrape_end) AS fromnow'))->where('type','=','cards')->first(),
                  "boosters" => DB::table('scrape_info')->select(DB::raw('TO_SECONDS(NOW())-TO_SECONDS(scrape_end) AS fromnow'))->where('type','=','boosters')->first() ];
  return View::make('profitableboosters')->with('boosters',$boosters)->with('scrapeinfo',$scrapeinfo);
});
