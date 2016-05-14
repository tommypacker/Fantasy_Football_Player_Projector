function loadJSON(data){
    $(document).ready(function()
    {
        var score1 = Math.round(data.players[0].score);
        var score2 = Math.round(data.players[1].score);
        var config1 = liquidFillGaugeDefaultSettings();
        config1.circleColor = "#FF7777";
        config1.textColor = "#FF4444";
        config1.waveTextColor = "#FFAAAA";
        config1.waveColor = "#FFDDDD";
        config1.circleThickness = 0.2;
        config1.textVertPosition = 0.2;
        config1.waveAnimateTime = 1500;
        var gauge1= loadLiquidFillGauge("fillgauge1", score1, config1);
        $("#playerTwo").html(data.players[1].name);
        var config2 = liquidFillGaugeDefaultSettings();
        config2.circleColor = "#178BCA";
        config2.textColor = "#045681";
        config2.waveTextColor = "#A4DBf8";
        config2.waveColor = "#178BCA";
        config2.circleThickness = 0.2;
        config2.textVertPosition = 0.2;
        config2.waveAnimateTime = 1500;
        var guage2 = loadLiquidFillGauge("fillgauge2", score2, config2);
        $("#playerOne").html(data.players[0].name);
    });
}