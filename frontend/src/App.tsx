import { InputForm } from "@/components/InputForm";
import MainNav from "@/components/MainNav";
import UserNav from "@/components/UserNav";

export default function App() {
  return (
    <div className="flex flex-col">
      <MainNav className="mb-4" />
      <div className="flex flex-col items-center px-2 md:px-0">
        <div className="border border-slate-200 rounded-xl w-full lg:w-3/4 p-4">
          <h1 className="text-3xl font-bold underline pb-4 lg:px-2">
            Fracture Risk Calculator
          </h1>
          <InputForm />
        </div>
      </div>
    </div>
  );
}
