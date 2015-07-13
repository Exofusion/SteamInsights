<html>
  <head>
    <title>Steam Insights</title>
    {{ HTML::style('css/common.css') }}
	<meta name="description" content="Steam Market trading cards statistics, giving you insights into the marketplace">
	<meta http-equiv="content-type" content="text/html;charset=UTF-8">
  </head>
  <body>
	<div class="header_container">
		<div class="header_text">
		Steam Insights
		</div>
	</div>
    <div class="content">
    @yield('content')
    </div>
	
  @include('analytics')
  </body>
</html>