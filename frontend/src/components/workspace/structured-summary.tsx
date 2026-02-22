"use client"

import { useState } from "react"
import { useTranslations } from "next-intl"
import type { StructuredContribution } from "@/types"

interface StructuredSummaryProps {
  contribution: StructuredContribution
  paperIndex: number
  paperTitle: string
}

const FIELD_KEYS = [
  "problem",
  "method",
  "novelty",
  "dataset",
  "baseline",
  "results",
  "limitations",
  "future_work",
] as const

type FieldKey = (typeof FIELD_KEYS)[number]

const FIELD_TRANSLATION_MAP: Record<FieldKey, string> = {
  problem: "structuredProblem",
  method: "structuredMethod",
  novelty: "structuredNovelty",
  dataset: "structuredDataset",
  baseline: "structuredBaseline",
  results: "structuredResults",
  limitations: "structuredLimitations",
  future_work: "structuredFutureWork",
}

export function StructuredSummary({
  contribution,
  paperIndex,
  paperTitle,
}: StructuredSummaryProps) {
  const t = useTranslations("workspace")
  const [expanded, setExpanded] = useState(false)

  const availableFields = FIELD_KEYS.filter((key) => contribution[key])

  if (availableFields.length === 0) {
    return null
  }

  return (
    <div className="border border-zinc-200 dark:border-zinc-700 rounded-lg overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-4 py-3 flex items-center justify-between bg-zinc-50 dark:bg-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors"
      >
        <div className="flex items-center gap-2 text-left">
          <span className="font-medium text-blue-600 dark:text-blue-400">
            [{paperIndex}]
          </span>
          <span className="text-sm text-zinc-900 dark:text-zinc-100 line-clamp-1">
            {paperTitle}
          </span>
        </div>
        <svg
          className={`w-4 h-4 text-zinc-500 transition-transform ${
            expanded ? "rotate-180" : ""
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {expanded && (
        <div className="px-4 py-3 space-y-3 bg-white dark:bg-zinc-900">
          {availableFields.map((key) => (
            <div key={key}>
              <dt className="text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wide">
                {t(FIELD_TRANSLATION_MAP[key])}
              </dt>
              <dd className="mt-1 text-sm text-zinc-900 dark:text-zinc-100">
                {contribution[key]}
              </dd>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

interface StructuredSummaryListProps {
  papers: Array<{
    paper_id: string
    title: string
    structured_contribution: StructuredContribution | null
  }>
}

export function StructuredSummaryList({ papers }: StructuredSummaryListProps) {
  const t = useTranslations("workspace")

  const papersWithStructured = papers.filter((p) => p.structured_contribution)

  if (papersWithStructured.length === 0) {
    return null
  }

  return (
    <div className="border-t border-zinc-200 dark:border-zinc-700 mt-8 pt-6">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-4">
        {t("structuredTitle")}
      </h3>
      <div className="space-y-3">
        {papers.map((paper, index) =>
          paper.structured_contribution ? (
            <StructuredSummary
              key={paper.paper_id}
              contribution={paper.structured_contribution}
              paperIndex={index + 1}
              paperTitle={paper.title}
            />
          ) : null
        )}
      </div>
    </div>
  )
}
