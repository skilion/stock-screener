namespace StockScreenerWebApp.Models.StockScreenerDb
{
    public partial class CompanyOverview
    {
        public string Symbol { get; set; } = null!;
        public string AssetType { get; set; } = null!;
        public string Name { get; set; } = null!;
        public string Description { get; set; } = null!;
        public string Cik { get; set; } = null!;
        public string Exchange { get; set; } = null!;
        public string Currency { get; set; } = null!;
        public string Country { get; set; } = null!;
        public string Sector { get; set; } = null!;
        public string Industry { get; set; } = null!;
        public string Address { get; set; } = null!;
        public string FiscalYearEnd { get; set; } = null!;
        public DateTime LatestQuarter { get; set; }
        public long MarketCapitalization { get; set; }
        public long? Ebitda { get; set; }
        public double? Peratio { get; set; }
        public double? Pegratio { get; set; }
        public double? BookValue { get; set; }
        public double? DividendPerShare { get; set; }
        public double? DividendYield { get; set; }
        public double? Eps { get; set; }
        public double? RevenuePerShareTtm { get; set; }
        public double? ProfitMargin { get; set; }
        public double? OperatingMarginTtm { get; set; }
        public double? ReturnOnAssetsTtm { get; set; }
        public double? ReturnOnEquityTtm { get; set; }
        public long? RevenueTtm { get; set; }
        public long? GrossProfitTtm { get; set; }
        public double? DilutedEpsttm { get; set; }
        public double? QuarterlyEarningsGrowthYoy { get; set; }
        public double? QuarterlyRevenueGrowthYoy { get; set; }
        public double? AnalystTargetPrice { get; set; }
        public double? TrailingPe { get; set; }
        public double? ForwardPe { get; set; }
        public double? PriceToSalesRatioTtm { get; set; }
        public double? PriceToBookRatio { get; set; }
        public double? EvtoRevenue { get; set; }
        public double? EvtoEbitda { get; set; }
        public double? Beta { get; set; }
        public double? _52weekHigh { get; set; }
        public double? _52weekLow { get; set; }
        public double? _50dayMovingAverage { get; set; }
        public double? _200dayMovingAverage { get; set; }
        public long? SharesOutstanding { get; set; }
        public DateTime? DividendDate { get; set; }
        public DateTime? ExDividendDate { get; set; }

        public virtual Symbol SymbolNavigation { get; set; } = null!;
    }
}
