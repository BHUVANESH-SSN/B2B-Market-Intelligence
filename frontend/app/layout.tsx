import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

export const metadata: Metadata = {
  title: "B2B Market Intelligence",
  description: "Market intelligence platform with Clerk authentication",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">
        <ClerkProvider>
          <main className="flex flex-1 flex-col">{children}</main>
        </ClerkProvider>
      </body>
    </html>
  );
}
