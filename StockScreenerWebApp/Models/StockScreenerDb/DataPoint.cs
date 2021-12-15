namespace StockScreenerWebApp.Models.StockScreenerDb
{
    public partial class DataPoint
    {
        public string Symbol { get; set; } = null!;
        public DateTime Date { get; set; }
        public double Open { get; set; }
        public double High { get; set; }
        public double Low { get; set; }
        public double Close { get; set; }
        public double AdjustedClose { get; set; }
        public long Volume { get; set; }
        public double DividendAmount { get; set; }
        public double SplitCoefficient { get; set; }

        public virtual Symbol SymbolNavigation { get; set; } = null!;
    }
}
