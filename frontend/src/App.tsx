import { ThemeProvider } from "@/components/Theme/theme-provider";
import { InputForm } from "@/components/InputForm";
import MainNav from "@/components/MainNav";
import { Toaster } from "react-hot-toast";

export default function App() {
  return (
    <ThemeProvider defaultTheme="light">
      <div className="flex flex-col bg-background">
        <MainNav className="mb-4" />
        <div className="flex flex-col items-center px-2 md:px-0">
          <InputForm />
        </div>
        <Toaster />
      </div>
    </ThemeProvider>
  );
}
