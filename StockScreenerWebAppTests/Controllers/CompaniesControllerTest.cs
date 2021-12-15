using StockScreenerWebApp.Controllers;
using Xunit;

namespace StockScreenerWebAppTests
{
    public class CompaniesControllerTest
    {
        [Fact]
        public void TestChangeComputeChange()
        {
            // Arrange
            double[] prices = new double[] { 10, 15 };

            // Act
            double change = CompaniesController.ComputeChange(prices, prices.Length - 1) ?? 0;

            // Assert
            Assert.Equal(.5, change, 5);
        }

        [Fact]
        public void TestComputeVolatility()
        {
            // Arrange
            double[] prices = new double[] { 52, 41, 58, 63, 49, 50, 72 };

            // Act
            double vol = CompaniesController.ComputeVolatilty(prices, prices.Length) ?? 0;

            // Assert
            Assert.Equal(10.23067284, vol, 5);
        }
    }
}