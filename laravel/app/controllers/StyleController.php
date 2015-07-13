<?php

class StyleController extends BaseController {
	public static function hexGradient($inputVal, $neutralColor, $minVal, $maxVal, $riseStep, $fallStep, $maxSteps)
	{
		if ($inputVal > $maxVal)
		{
			$neutralColor += $maxSteps * $riseStep;
		}
		else if ($inputVal < $minVal)
		{
			$neutralColor += $maxSteps * $fallStep;
		}
		else
		{
			$middle = ($maxVal + $minVal)/2;
			
			if ($inputVal > $middle)
			{
				$neutralColor += ($riseStep*(int) ($maxSteps*(($inputVal-$middle)/abs($maxVal-$minVal))));
			}
			else if ($inputVal < $middle)
			{
				$neutralColor += ($fallStep*(int) ($maxSteps*(($inputVal-$middle)/abs($maxVal-$minVal))));
			}
		}
		
		return str_pad(dechex($neutralColor),6,"0",STR_PAD_LEFT);
	}

	public static function getProfitColor($profit)
	{
		return StyleController::hexGradient($profit, 0xCCCC00, -.05, .10, -65536, 256, 127);
	}

	public static function getRiskColor($risk)
	{
		return StyleController::hexGradient($risk, 0xCCCC00, 0, .10, -256, 65536, 127);
	}
}
