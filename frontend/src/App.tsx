import { InputForm } from "@/components/InputForm";
import MainNav from "@/components/MainNav";
import UserNav from "@/components/UserNav";

export default function App() {
  return (
    <div className="flex flex-col">
      <div className="border-b mb-4">
        <div className="grid grid-cols-3 h-16 items-center px-4 lg:px-8">
          <a href="#">
            <h1 className="text-2xl font-bold mr-auto">Bono AI</h1>
          </a>
          <MainNav />
          <div className="flex items-end ml-auto">
            <UserNav />
          </div>
        </div>
      </div>
      <div className="flex flex-col items-center">
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
