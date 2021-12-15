using StockScreenerWebApp.Models.StockScreenerDb;

namespace StockScreenerWebApp.Models
{
    public class Overview
    {
        public CompanyOverview CompanyOverview { get; set; } = null!;
        public string TimeseriesJson { get; set; } = null!;
    }
}
