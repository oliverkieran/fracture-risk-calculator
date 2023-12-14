import { ThemeProvider } from "@/components/Theme/theme-provider";
import { InputForm } from "@/components/InputForm";
import MainNav from "@/components/MainNav";

export default function App() {
  return (
    <ThemeProvider defaultTheme="dark">
      <div className="flex flex-col bg-background">
        <MainNav className="mb-4" />
        <div className="flex flex-col items-center px-2 md:px-0">
          <div className="border border-border rounded-xl w-full lg:w-3/4 p-4">
            <h1 className="text-3xl font-bold text-foreground py-4 lg:px-2">
              Fracture Risk Calculator
            </h1>
            <InputForm />
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}
