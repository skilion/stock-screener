namespace StockScreenerWebApp.Models.StockScreenerDb
{
    public partial class Symbol
    {
        public Symbol()
        {
            DataPoints = new HashSet<DataPoint>();
        }

        public string Symbol1 { get; set; } = null!;
        public DateTime? LastUpdated { get; set; }

        public virtual CompanyOverview CompanyOverview { get; set; } = null!;
        public virtual ICollection<DataPoint> DataPoints { get; set; }
    }
}
