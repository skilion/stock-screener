using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StockScreenerWebApp.Models;
using StockScreenerWebApp.Models.StockScreenerDb;
using System.Reflection;
using System.Text.Json;

namespace StockScreenerWebApp.Controllers
{
    public class CompaniesController : Controller
    {
        private readonly StockScreenerDbContext context;
        private static readonly DateTime Epoch = new(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        private static CompanyOverview[] CompanyList = Array.Empty<CompanyOverview>();
        private static CompanyPerformance[] CompanyPerformanceList = Array.Empty<CompanyPerformance>();

        public CompaniesController(StockScreenerDbContext context)
        {
            this.context = context;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult List()
        {
            EnsureCompanyListIsLoaded();

            var query = CompanyList as IEnumerable<CompanyOverview>;
            var filters = Request.Query["filter"];
            foreach (var filter in filters)
            {
                query = ApplyCompanyFilter(query, filter);
            }

            return View(query.ToList());
        }

        public IActionResult Overview(string id)
        {
            return View(new Overview
            {
                CompanyOverview = context.CompanyOverviews
                    .Where(overview => overview.Symbol == id)
                    .AsNoTracking()
                    .Single(),
                TimeseriesJson = LastYearTimeSeriesJson(id),
            });
        }

        private void EnsureCompanyListIsLoaded()
        {
            if (CompanyList.Length == 0)
            {
                CompanyList = context.CompanyOverviews
                    .AsNoTracking()
                    .ToArray();
                /*CompanyPerformanceList = CompanyList
                    .Select(c => GetCompanyPerformance(c.Symbol, c.Name))
                    .ToArray();*/
            }
        }

        private string LastYearTimeSeriesJson(string symbol)
        {
            return JsonSerializer.Serialize(LastYearTimeseries(symbol)
                .Select(p => new object[]
                {
                    (long) (p.Date - Epoch).TotalMilliseconds,
                    new []
                    {
                        p.Open,
                        p.High,
                        p.Low,
                        p.Close
                    }
                })
                .ToArray()
            );
        }

        private DataPoint[] LastYearTimeseries(string symbol)
        {
            DateTime lastYear = DateTime.Today.AddYears(-1);
            return context.DataPoints
                .Where(p => p.Symbol == symbol)
                .Where(p => p.Date >= lastYear)
                .AsNoTracking()
                .ToArray();
        }

        private CompanyPerformance GetCompanyPerformance(string symbol, string name)
        {
            var adjustedPrices = GetAdjustedPrice1Y(symbol);
            return new CompanyPerformance
            {
                Symbol = symbol,
                Name = name,
                Price = adjustedPrices[^1],
                Change1d = ComputeChange(adjustedPrices, 1),
                Change1w = ComputeChange(adjustedPrices, 5),
                Change1m = ComputeChange(adjustedPrices, 21),
                Change3m = ComputeChange(adjustedPrices, 63),
                Change6m = ComputeChange(adjustedPrices, 126),
                Change1Y = ComputeChange(adjustedPrices, 252),
                Vol1w = ComputeVolatilty(adjustedPrices, 5),
                Vol1m = ComputeVolatilty(adjustedPrices, 21),
            };
        }

        private double[] GetAdjustedPrice1Y(string symbol)
        {
            DateTime lastYear = DateTime.Today.AddYears(-1);
            return context.DataPoints
                .Where(p => p.Symbol == symbol)
                .Where(p => p.Date >= lastYear)
                .OrderBy(p => p.Date)
                .Select(p => p.AdjustedClose)
                .ToArray();
        }

        public static double? ComputeChange(double[] prices, int days)
        {
            if (prices.Length > days)
            {
                return (prices[^1] - prices[^(days + 1)]) / prices[^(days + 1)];
            }
            return null;
        }

        public static double? ComputeVolatilty(double[] prices, int days)
        {
            if (prices.Length >= days)
            {
                var priceSlice = prices[^days .. ^0];
                double mean = priceSlice.Average();
                double variance = priceSlice.Select(p => (p - mean)*(p - mean)).Sum() / (days - 1);
                return Math.Sqrt(variance);
            }
            return null;
        }

        private static IEnumerable<CompanyOverview> ApplyCompanyFilter(IEnumerable<CompanyOverview> query, string filter)
        {
            if (filter.Length > 0)
            {
                var conditionIndex = filter.IndexOfAny(new char[] { '<', '>' });
                if (conditionIndex == -1)
                {
                    throw new ArgumentException($"No condition in filter {filter}");
                }
                var filterName = filter[..conditionIndex];
                var property = FilterToCompanyOverviewPropertyInfo(filterName);
                var condition = filter[conditionIndex];
                var value = ParseNumber(filter[(conditionIndex + 1)..]);
                return condition switch
                {
                    '<' => query.Where(company => Convert.ToDouble(property.GetValue(company)) < value),
                    '>' => query.Where(company => Convert.ToDouble(property.GetValue(company)) > value),
                    _ => throw new Exception()
                };
            }
            return query;
        }

        private static double ParseNumber(string value)
        {
            double multiplier = 1;
            if (value[^1] == 't' || value[^1] == 'T')
            {
                multiplier = 1e12;
                value = value[..^1];
            }
            else if (value[^1] == 'b' || value[^1] == 'B')
            {
                multiplier = 1e9;
                value = value[..^1];
            }
            else if (value[^1] == 'm' || value[^1] == 'M')
            {
                multiplier = 1e6;
                value = value[..^1];
            }
            else if (value[^1] == 'k' || value[^1] == 'K')
            {
                multiplier = 1e3;
                value = value[..^1];
            }
            return Convert.ToDouble(value) * multiplier;
        }

        private static PropertyInfo FilterToCompanyOverviewPropertyInfo(string filter)
        {
            return filter switch
            {
                "MktCap" => typeof(CompanyOverview).GetProperty("MarketCapitalization")!,
                "EBITDA" => typeof(CompanyOverview).GetProperty("Ebitda")!,
                "P/E" => typeof(CompanyOverview).GetProperty("Peratio")!,
                "PEG" => typeof(CompanyOverview).GetProperty("Pegratio")!,
                "B/V" => typeof(CompanyOverview).GetProperty("BookValue")!,
                "DPS" => typeof(CompanyOverview).GetProperty("DividendPerShare")!,
                "DividendYield" => typeof(CompanyOverview).GetProperty("DividendYield")!,
                "EPS" => typeof(CompanyOverview).GetProperty("Eps")!,
                "ProfitMargin" => typeof(CompanyOverview).GetProperty("ProfitMargin")!,
                _ => throw new ArgumentException("Invalid filter name"),
            };
        }
    }
}
