using Microsoft.EntityFrameworkCore;
using StockScreenerWebApp.Models.StockScreenerDb;

namespace StockScreenerWebApp
{
    public partial class StockScreenerDbContext : DbContext
    {
        public StockScreenerDbContext()
        {
        }

        public StockScreenerDbContext(DbContextOptions<StockScreenerDbContext> options)
            : base(options)
        {
        }

        public virtual DbSet<CompanyOverview> CompanyOverviews { get; set; } = null!;
        public virtual DbSet<DataPoint> DataPoints { get; set; } = null!;
        public virtual DbSet<Symbol> Symbols { get; set; } = null!;

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<CompanyOverview>(entity =>
            {
                entity.HasKey(e => e.Symbol)
                    .HasName("PK__CompanyO__B7CC3F00FB40BA76");

                entity.ToTable("CompanyOverview");

                entity.Property(e => e.Symbol)
                    .HasMaxLength(10)
                    .IsUnicode(false);

                entity.Property(e => e.Address)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.AssetType)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.Cik)
                    .HasMaxLength(255)
                    .IsUnicode(false)
                    .HasColumnName("CIK");

                entity.Property(e => e.Country)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.Currency)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.Description)
                    .HasMaxLength(5000)
                    .IsUnicode(false);

                entity.Property(e => e.DilutedEpsttm).HasColumnName("DilutedEPSTTM");

                entity.Property(e => e.DividendDate).HasColumnType("date");

                entity.Property(e => e.Ebitda).HasColumnName("EBITDA");

                entity.Property(e => e.Eps).HasColumnName("EPS");

                entity.Property(e => e.EvtoEbitda).HasColumnName("EVToEBITDA");

                entity.Property(e => e.EvtoRevenue).HasColumnName("EVToRevenue");

                entity.Property(e => e.ExDividendDate).HasColumnType("date");

                entity.Property(e => e.Exchange)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.FiscalYearEnd)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.ForwardPe).HasColumnName("ForwardPE");

                entity.Property(e => e.GrossProfitTtm).HasColumnName("GrossProfitTTM");

                entity.Property(e => e.Industry)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.LatestQuarter).HasColumnType("date");

                entity.Property(e => e.Name)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.OperatingMarginTtm).HasColumnName("OperatingMarginTTM");

                entity.Property(e => e.Pegratio).HasColumnName("PEGRatio");

                entity.Property(e => e.Peratio).HasColumnName("PERatio");

                entity.Property(e => e.PriceToSalesRatioTtm).HasColumnName("PriceToSalesRatioTTM");

                entity.Property(e => e.QuarterlyEarningsGrowthYoy).HasColumnName("QuarterlyEarningsGrowthYOY");

                entity.Property(e => e.QuarterlyRevenueGrowthYoy).HasColumnName("QuarterlyRevenueGrowthYOY");

                entity.Property(e => e.ReturnOnAssetsTtm).HasColumnName("ReturnOnAssetsTTM");

                entity.Property(e => e.ReturnOnEquityTtm).HasColumnName("ReturnOnEquityTTM");

                entity.Property(e => e.RevenuePerShareTtm).HasColumnName("RevenuePerShareTTM");

                entity.Property(e => e.RevenueTtm).HasColumnName("RevenueTTM");

                entity.Property(e => e.Sector)
                    .HasMaxLength(255)
                    .IsUnicode(false);

                entity.Property(e => e.TrailingPe).HasColumnName("TrailingPE");

                entity.Property(e => e._200dayMovingAverage).HasColumnName("200DayMovingAverage");

                entity.Property(e => e._50dayMovingAverage).HasColumnName("50DayMovingAverage");

                entity.Property(e => e._52weekHigh).HasColumnName("52WeekHigh");

                entity.Property(e => e._52weekLow).HasColumnName("52WeekLow");

                entity.HasOne(d => d.SymbolNavigation)
                    .WithOne(p => p.CompanyOverview)
                    .HasForeignKey<CompanyOverview>(d => d.Symbol)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__CompanyOv__Symbo__787EE5A0");
            });

            modelBuilder.Entity<DataPoint>(entity =>
            {
                entity.HasKey(e => new { e.Symbol, e.Date })
                    .HasName("PK__DataPoin__C0BFB8D0474257E5");

                entity.ToTable("DataPoint");

                entity.Property(e => e.Symbol)
                    .HasMaxLength(10)
                    .IsUnicode(false);

                entity.Property(e => e.Date).HasColumnType("date");

                entity.HasOne(d => d.SymbolNavigation)
                    .WithMany(p => p.DataPoints)
                    .HasForeignKey(d => d.Symbol)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK__DataPoint__Symbo__6FE99F9F");
            });

            modelBuilder.Entity<Symbol>(entity =>
            {
                entity.HasKey(e => e.Symbol1)
                    .HasName("PK__Symbol__B7CC3F0042501C4A");

                entity.ToTable("Symbol");

                entity.Property(e => e.Symbol1)
                    .HasMaxLength(10)
                    .IsUnicode(false)
                    .HasColumnName("Symbol");

                entity.Property(e => e.LastUpdated).HasColumnType("datetime");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
