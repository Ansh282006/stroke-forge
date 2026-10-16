import { create } from "zustand";
import type { JobInfo } from "../api/client";

type State = {
  job: JobInfo | null;
  setJob: (j: JobInfo | null) => void;
};

export const useJobStore = create<State>((set) => ({
  job: null,
  setJob: (j) => set({ job: j })
}));