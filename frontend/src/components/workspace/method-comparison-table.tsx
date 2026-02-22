"use client"

import { useState } from "react"
import { useTranslations } from "next-intl"
import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import type { Paper } from "@/types"

interface MethodComparisonTableProps {
  papers: Paper[]
}

export function MethodComparisonTable({ papers }: MethodComparisonTableProps) {
  const t = useTranslations("workspace")
  const [expanded, setExpanded] = useState(false)

  const papersWithStructured = papers.filter((p) => p.structured_contribution)

  if (papersWithStructured.length === 0) {
    return null
  }

  return (
    <div className="border-t border-zinc-200 dark:border-zinc-700 mt-8 pt-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
          {t("comparisonTitle")}
        </h3>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? t("comparisonHide") : t("comparisonShow")}
        </Button>
      </div>

      {expanded && (
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="min-w-[200px]">{t("comparisonPaper")}</TableHead>
                <TableHead className="min-w-[150px]">{t("comparisonMethod")}</TableHead>
                <TableHead className="min-w-[120px]">{t("comparisonDataset")}</TableHead>
                <TableHead className="min-w-[120px]">{t("comparisonBaseline")}</TableHead>
                <TableHead className="min-w-[150px]">{t("comparisonResults")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {papers.map((paper, index) => {
                const sc = paper.structured_contribution
                return (
                  <TableRow key={paper.paper_id}>
                    <TableCell>
                      <div className="max-w-[200px]">
                        <span className="font-medium text-blue-600 dark:text-blue-400">
                          [{index + 1}]
                        </span>{" "}
                        <span className="text-sm line-clamp-2">{paper.title}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-sm text-zinc-600 dark:text-zinc-400">
                      {sc?.method || t("structuredNotAvailable")}
                    </TableCell>
                    <TableCell className="text-sm text-zinc-600 dark:text-zinc-400">
                      {sc?.dataset || t("structuredNotAvailable")}
                    </TableCell>
                    <TableCell className="text-sm text-zinc-600 dark:text-zinc-400">
                      {sc?.baseline || t("structuredNotAvailable")}
                    </TableCell>
                    <TableCell className="text-sm text-zinc-600 dark:text-zinc-400">
                      {sc?.results || t("structuredNotAvailable")}
                    </TableCell>
                  </TableRow>
                )
              })}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}
