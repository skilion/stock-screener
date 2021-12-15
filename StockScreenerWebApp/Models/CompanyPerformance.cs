namespace StockScreenerWebApp.Models
{
    public class CompanyPerformance
    {
        public string Symbol { get; set; } = null!;
        public string Name { get; set; } = null!;
        public double Price { get; set; }
        public double? Change1d { get; set; }
        public double? Change1w { get; set; }
        public double? Change1m { get; set; }
        public double? Change3m { get; set; }
        public double? Change6m { get; set; }
        public double? Change1Y { get; set; }
        public double? Vol1w { get; set; }
        public double? Vol1m { get; set; }
    }
}
