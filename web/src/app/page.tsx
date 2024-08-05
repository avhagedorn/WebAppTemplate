"use client";

import demoData from "../public/demoData/dummyGraph.json";
import demoGoogData from "../public/demoData/goog.json";
import demoCompareData from "../public/demoData/compare.json";
import { useRouter } from "next/navigation";
import { useQuery } from "react-query";
import { fetchSS } from "@/lib/fetch";
import ContentWrapper from "@/components/ContentWrapper";
import PositionsTable from "@/components/PositionsTable";
import PriceChange from "@/components/PriceChange";
import CompareGraphWrapper from "@/components/CompareGraphWrapper";
import StockPriceChart from "@/components/StockPriceChart";
import Statistics from "@/components/Statistics";
import DateGraph from "@/components/DateGraph";
import { Timeframe } from "@/types";
import { LuArrowRightLeft } from "react-icons/lu";
import { FiExternalLink } from "react-icons/fi";
import TruncatedText from "@/components/TruncatedText";

export default function Home() {
  const router = useRouter();
  const { data, isFetching } = useQuery("user", () => fetchSS("/user/me"));

  if (isFetching) {
    return null;
  } else if (data) {
    router.push("/home");
  } else {
    return (
      <ContentWrapper className="bg-gradient-to-r from-white to-emerald-50">
        <div className="flex min-h-screen flex-col items-center p-24">
          <header className="flex flex-col items-center">
            <h1 className="text-6xl font-bold">AlphaTracker</h1>
            <p className="text-3xl text-center mt-4">
              Track your portfolio against the market
            </p>
            <a
              className="bg-emerald-500 hover:bg-emerald-700 text-white font-semibold py-3 px-6 mt-16 rounded shadow-lg text-2xl"
              href={"/auth/register"}
            >
              Track your portfolio
            </a>
          </header>
          {/* Main Portfolio */}
          <div className="flex flex-row justify-center items-center w-full space-x-16 mt-32">
            <div className="w-1/3">
              <h1 className="text-4xl font-bold">
                Benchmark Your Portfolio 🚀
              </h1>
              <p className="text-2xl mt-4">
                Track your portfolio against common indices like the S&P 500, or
                create custom benchmarks. Start generating alpha today!
              </p>
            </div>
            <div className="transform skew-y-2 w-1/2 bg-white p-4 rounded-xl shadow-lg">
              <h1 className="text-4xl font-bold">$3,500</h1>
              <PriceChange
                percentChange={0.1}
                valueChange={350}
                subText="Today"
              />
              <PriceChange
                percentChange={0.1}
                valueChange={350}
                subText="Alpha"
              />
              <CompareGraphWrapper
                width={"100%"}
                height={300}
                margin={{ top: 10, right: 30, left: 20, bottom: 10 }}
                data={demoData}
                ticks={4}
                lineWidth={3}
                hideLegend
              />
              <PositionsTable
                data={[
                  {
                    ticker: "AAPL",
                    shares: 1000,
                    equity_value: 1000,
                    return_percent: 0.1,
                    return_value: 100,
                    alpha_percent: 0.05,
                    alpha_value: 50,
                    realized_alpha: 0,
                    realized_value: 0,
                  },
                  {
                    ticker: "GOOGL",
                    shares: 2000,
                    equity_value: 2000,
                    return_percent: 0.2,
                    return_value: 400,
                    alpha_percent: 0.1,
                    alpha_value: 200,
                    realized_alpha: 0,
                    realized_value: 0,
                  },
                  {
                    ticker: "MSFT",
                    shares: 1500,
                    equity_value: 1500,
                    return_percent: 0.15,
                    return_value: 225,
                    alpha_percent: 0.075,
                    alpha_value: 112.5,
                    realized_alpha: 0,
                    realized_value: 0,
                  },
                ]}
              />
            </div>
          </div>

          {/* Stock Graph */}
          <div className="flex flex-row justify-center items-center w-full space-x-16 mt-32">
            <div className="transform -skew-y-2 w-1/2 bg-white p-4 rounded-xl shadow-lg">
              <div className="flex justify-between items-start">
                <div>
                  <h1 className="text-3xl font-bold mb-4">
                    GOOGL - Alphabet Inc.
                  </h1>
                </div>
                <div>
                  <div className="flex flex-col items-start">
                    <button onClick={() => {}} className="mt-4">
                      <div className="flex items-center justify-center text-lg">
                        <LuArrowRightLeft className="mr-2" size={18} />
                        Compare
                      </div>
                    </button>
                  </div>
                </div>
              </div>
              <PriceChange
                percentChange={demoGoogData.total_return_percent}
                valueChange={demoGoogData.total_return}
                subText={"Today"}
              />
              <PriceChange
                percentChange={
                  demoGoogData.total_return_percent -
                  demoGoogData.total_return_percent_spy
                }
                valueChange={
                  demoGoogData.total_return - demoGoogData.total_return_spy
                }
                subText="Alpha"
              />
              <div className="mt-4">
                <DateGraph
                  width={"100%"}
                  height={300}
                  data={demoGoogData.points}
                  lineWidth={3}
                  leftLineName={"GOOG"}
                  animationDuration={500}
                  selectedTimeframe={Timeframe.DAY}
                  handleTimeframeChange={() => {}}
                />
              </div>
              <div className="mt-8">
                <div className="flex items-center space-x-2">
                  <h1 className="text-2xl font-bold">Company</h1>
                  <a href={demoGoogData.stats.website} target="_blank">
                    <FiExternalLink size={18} />
                  </a>
                </div>
                <TruncatedText text={demoGoogData.stats.description} />
                <div className="mt-8">
                  <h1 className="text-2xl font-bold">Statistics</h1>
                  <Statistics
                    cards={[
                      {
                        title: "Financials",
                        statistics: [
                          {
                            title: "Market Cap",
                            value: "2.18T",
                          },
                          {
                            title: "EPS",
                            value: "6.52",
                          },
                          {
                            title: "Dividend Yield",
                            value: "0.45%",
                            tooltip:
                              "The dividend yield is the annual dividend income per " +
                              "share divided by the price per share.",
                          },
                          {
                            title: "Revenue Growth (YoY)",
                            value: "15.4%",
                          },
                        ],
                      },
                      {
                        title: "Valuation",
                        statistics: [
                          {
                            title: "PE Ratio",
                            value: "27.21",
                            tooltip:
                              "The price-to-earnings (P/E) ratio is the ratio for " +
                              "valuing a company that measures its current share price " +
                              "relative to its per-share earnings.",
                          },
                          {
                            title: "Forward PE",
                            value: "22.46",
                            tooltip:
                              "The forward price-to-earnings (P/E) ratio is a variation of " +
                              "the P/E ratio that uses forecasted earnings for the P/E calculation.",
                          },
                          {
                            title: "EV to EBITDA",
                            value: "19.32",
                            tooltip:
                              "The EV/EBITDA ratio is a valuation metric used to compare a " +
                              "company's enterprise value to its earnings before interest, " +
                              "taxes, depreciation, and amortization.",
                          },
                          {
                            title: "52W Range",
                            value: (
                              <StockPriceChart
                                low={demoGoogData.stats.fifty_two_week_low}
                                high={demoGoogData.stats.fifty_two_week_high}
                                current={demoGoogData.last_price}
                              />
                            ),
                          },
                        ],
                      },
                      {
                        title: "Ratios",
                        statistics: [
                          {
                            title: "Short Ratio",
                            value: "1.78",
                            tooltip:
                              "The short ratio is the number of shares sold short divided by " +
                              "the average daily volume. It's used to determine how long it will " +
                              "take short sellers, on average, to cover their positions.",
                          },
                          {
                            title: "PEG Ratio",
                            value: "1.41",
                            tooltip:
                              "The PEG ratio is a valuation metric for determining the relative " +
                              "trade-off between the price of a stock, the earnings generated per " +
                              "share (EPS), and the company's expected growth.",
                          },
                          {
                            title: "Beta",
                            value: "1.02",
                            tooltip:
                              "Beta is a measure of a stock's volatility in relation to the market.",
                          },
                        ],
                      },
                      {
                        title: "Margins",
                        statistics: [
                          {
                            title: "Gross Margins",
                            value: "57.47%",
                            tooltip:
                              "The gross margin represents the percentage of total revenue that the " +
                              "company retains after incurring the direct costs associated with " +
                              "producing the goods and services sold by the company.",
                          },
                          {
                            title: "Operating Margins",
                            value: "32.52%",
                            tooltip:
                              "The operating margin measures how much profit a company makes on a " +
                              "dollar of sales after paying for variable costs of production, such " +
                              "as wages and raw materials, but before paying interest or tax.",
                          },
                          {
                            title: "Profit Margins",
                            value: "25.9%",
                            tooltip:
                              "The profit margin is a ratio of a company's profit (sales minus all " +
                              "expenses) divided by its revenue.",
                          },
                        ],
                      },
                      {
                        title: "Profitability",
                        statistics: [
                          {
                            title: "Free Cash Flow Yield",
                            value: "2.52%",
                            tooltip:
                              "The free cash flow yield is a financial ratio that measures a " +
                              "company's ability to generate free cash flow relative to its " +
                              "market capitalization.",
                          },
                          {
                            title: "Return on Equity",
                            value: "29.76%",
                            tooltip:
                              "Return on equity (ROE) is a measure of financial performance calculated " +
                              "by dividing net income by shareholders' equity.",
                          },
                          {
                            title: "Return on Assets",
                            value: "15.61%",
                            tooltip:
                              "Return on assets (ROA) is an indicator of how profitable a company is " +
                              "relative to its total assets.",
                          },
                        ],
                      },
                      {
                        title: "Debt",
                        statistics: [
                          {
                            title: "Cash",
                            value: "$108.09B",
                          },
                          {
                            title: "Debt",
                            value: "$28.38B",
                          },
                          {
                            title: "Current Ratio",
                            value: "2.15",
                            tooltip:
                              "The current ratio is a liquidity ratio that measures a company's ability to pay short-term obligations or those due within one year.",
                          },
                        ],
                      },
                    ]}
                  />
                </div>
              </div>
            </div>
            <div className="w-1/3">
              <h1 className="text-4xl font-bold">
                Analyze Stocks and Your Investing Strategies 💡
              </h1>
              <p className="text-2xl mt-4">
                Compare your stock picks against the market. Analyze your
                investments with detailed statistics and charts.
              </p>
            </div>
          </div>

          {/* Compare Graph */}
          <div className="flex flex-row justify-center items-center w-full space-x-16 mt-32">
            <div className="w-1/3">
              <h1 className="text-4xl font-bold">
                Compare Equities and Portfolios 📊
              </h1>
              <p className="text-2xl mt-4">
                Compare your portfolio against other portfolios or individual
                equities. Analyze your investments with detailed statistics and
                charts.
              </p>
            </div>
            <div className="transform skew-y-2 w-1/3 bg-white p-4 rounded-xl shadow-lg">
              <div className="h-10 flex flex-row items-end">
                <p className="text-3xl font-bold text-emerald-500 cursor-pointer">
                  {demoCompareData.left_name}
                </p>
                <span className="mx-2 text-3xl font-bold">vs</span>
                <p className="text-3xl font-bold text-indigo-500 cursor-pointer">
                  {demoCompareData.right_name}
                </p>
              </div>
              <p>
                {demoCompareData.left_name} has returned{" "}
                <span className="font-bold" style={{ color: "#10b981" }}>
                  {demoCompareData.total_return_left}%
                </span>{" "}
                , which is{" "}
                <span className="font-bold">
                  {Math.abs(
                    demoCompareData.total_return_left -
                      demoCompareData.total_return_right,
                  )}
                  % less
                </span>{" "}
                than {demoCompareData.right_name}, which has returned{" "}
                <span className="font-bold" style={{ color: "#6366f1" }}>
                  {demoCompareData.total_return_percent_right}%
                </span>
                .
              </p>
              <div className="mt-4">
                <DateGraph
                  width={"100%"}
                  height={300}
                  data={demoCompareData.points}
                  selectedTimeframe={Timeframe.DAY}
                  handleTimeframeChange={() => {}}
                  lineWidth={3}
                  animationDuration={500}
                  leftLineName={demoCompareData.left_name}
                  rightLineName={demoCompareData.right_name}
                />
              </div>
            </div>
          </div>

          {/* CTA */}
          <a
            className="bg-emerald-500 hover:bg-emerald-700 text-white font-semibold py-3 px-6 mt-32 rounded shadow-lg text-2xl"
            href={"/auth/register"}
          >
            Join Today
          </a>
        </div>
      </ContentWrapper>
    );
  }
}
