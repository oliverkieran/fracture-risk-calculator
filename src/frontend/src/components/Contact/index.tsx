import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Contact() {
  return (
    <div className="w-full lg:min-h-[600px] xl:min-h-[800px]">
      <div className="flex justify-center">
        <div className="flex items-center justify-center mx-12 w-1/2">
          <div className="mx-auto grid gap-6 border dark:border-border rounded-xl bg-muted dark:bg-card p-8 w-full">
            <div className="grid gap-2 text-center">
              <h1 className="text-4xl font-bold dark:text-foreground">
                Contact Us!
              </h1>
              <p className="dark:-text--secondary-foreground">
                We are looking forward to hear from you!
              </p>
            </div>
            <div className="grid gap-2">
              <form className="flex flex-col w-full space-y-4">
                <Label htmlFor="name">Name</Label>
                <Input id="name" placeholder="Name" />
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" placeholder="Email" />
                <Label htmlFor="message">Message</Label>
                <textarea
                  id="message"
                  className="w-full h-32 p-2 border rounded-md dark:border-border dark:bg-card dark:text-foreground"
                  placeholder="Message"
                />
                <div className="flex justify-center">
                  <Button type="submit" className="w-40">
                    Submit
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </div>
        <div className="flex items-center w-1/2 max-w-md h-full">
          <img
            src="https://images.unsplash.com/photo-1586769852044-692d6e3703f0?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            alt="random"
            className="w-full object-cover rounded-xl"
          />
        </div>
      </div>
    </div>
  );
}
