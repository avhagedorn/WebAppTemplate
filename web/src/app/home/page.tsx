"use client";

import PositionsTable from "@/components/PositionsTable";
import PriceChange from "@/components/PriceChange";
import { useState } from "react";
import demoData from "../../public/demoData/dummyGraph.json";
import DateGraph from "@/components/DateGraph";
import { Timeframe } from "@/types";
import StrategyList from "@/components/StrategyList";
import ContentWrapper from "@/components/ContentWrapper";
import { useQuery } from "react-query";
import { fetchSS } from "@/lib/fetch";
import { fmtDollars, timeframeToDisplayString } from "@/lib/utils";
import ExercisedPositionsTable from "@/components/ExercisedPositionsTable";

export default function Home() {
  const [timeframe, setTimeframe] = useState<Timeframe>(Timeframe.DAY);
  const { data, status, error } = useQuery(["summary", timeframe], () =>
    fetchSS(`/chart/summary?timeframe=${timeframe}`),
  );

  const {
    data: positionsData,
    status: positionsStatus,
    error: positionsError,
  } = useQuery("positions", () => fetchSS("/positions/all"));

  return (
    <ContentWrapper hideFooter>
      <div className="flex min-h-screen flex-col items-center">
        <div className="flex w-screen">
          <div className="flex-1 p-8">
            {status === "loading" && <div className="shimmer h-16 w-32 mb-4" />}
            {status === "success" && (
              <h1 className="text-6xl font-bold mb-4">
                {fmtDollars(data?.last_price || 0)}
              </h1>
            )}
            <PriceChange
              loading={status === "loading"}
              percentChange={data?.total_return_percent || 0}
              valueChange={data?.total_return || 0}
              subText={timeframeToDisplayString(timeframe)}
            />
            <PriceChange
              loading={status === "loading"}
              percentChange={
                data?.total_return_percent - data?.total_return_percent_spy || 0
              }
              valueChange={data?.total_return - data?.total_return_spy || 0}
              subText="Alpha"
            />
            <div className="mt-4">
              <DateGraph
                width={"100%"}
                height={300}
                data={data?.points || demoData}
                selectedTimeframe={timeframe}
                handleTimeframeChange={setTimeframe}
                lineWidth={4}
                animationDuration={500}
              />
            </div>

            <div className="mt-8">
              <PositionsTable
                data={positionsData}
                loading={positionsStatus === "loading"}
              />
            </div>

            <div className="mt-8">
              <ExercisedPositionsTable
                data={positionsData}
                loading={positionsStatus === "loading"}
                className="mt-8"
              />
            </div>
          </div>

          <div className="w-[500px] min-w-[500px] min-h-screen p-8 border-l-2 border-gray-300">
            <StrategyList />
          </div>
        </div>
      </div>
    </ContentWrapper>
  );
}
