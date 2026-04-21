"use client";

import { useEffect, useState } from "react";
import UploadBox from "../components/UploadBox";
import ChatBox from "../components/ChatBox";
import StatusCard from "../components/StatusCard";
import { getKnowledgeBaseStatus } from "../lib/api";

type KnowledgeBaseStatus = {
  documents_loaded: number;
  chunks_indexed: number;
  last_uploaded_document: string;
  status: string;
};

export default function HomePage() {
  const [kbStatus, setKbStatus] = useState<KnowledgeBaseStatus | null>(null);

  const loadStatus = async () => {
    try {
      const result = await getKnowledgeBaseStatus();
      setKbStatus(result);
    } catch (error) {
      console.error("Failed to load KB status");
    }
  };

  useEffect(() => {
    const fetchStatus = async () => {
      await loadStatus();
    };

    fetchStatus();
  }, []);

  return (
    <main className="min-h-screen bg-gray-100 px-6 py-10">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900">
            AskDocs AI
          </h1>
          <p className="mt-3 text-base text-gray-600">
            Upload PDFs, ask questions, and get grounded answers with sources.
          </p>
        </div>

        <div className="space-y-6">
          <UploadBox onUploadSuccess={loadStatus} />

          {kbStatus && (
            <StatusCard
              documentsLoaded={kbStatus.documents_loaded}
              chunksIndexed={kbStatus.chunks_indexed}
              lastUploadedDocument={kbStatus.last_uploaded_document}
              status={kbStatus.status}
            />
          )}

          <ChatBox isReady={!!kbStatus && kbStatus.documents_loaded > 0} />
        </div>
      </div>
    </main>
  );
}