import {
  Dialog,
  DialogContent,
  DialogDescription,
  // DialogFooter,
  DialogHeader,
  // DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import UploadSection from "./UploadSection";

export default function UploadButton() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <a
          className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44 cursor-pointer"
          target="_blank"
          rel="noopener noreferrer"
        >
          Upload File
        </a>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogDescription>
            <UploadSection />
          </DialogDescription>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
}
