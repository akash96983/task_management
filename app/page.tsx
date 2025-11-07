import Link from 'next/link';

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black px-4">
      <main className="flex flex-col items-center justify-center space-y-8 text-center">
        <h1 className="text-4xl font-bold text-zinc-900 dark:text-zinc-50">
          Welcome to Task Management
        </h1>
        <p className="text-lg text-zinc-600 dark:text-zinc-400 max-w-md">
          Organize your tasks efficiently and boost your productivity
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            href="/auth/login"
            className="px-6 py-3 bg-zinc-900 dark:bg-zinc-50 text-white dark:text-zinc-900 rounded-lg font-medium hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-colors"
          >
            Login
          </Link>
          <Link
            href="/auth/signup"
            className="px-6 py-3 border border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-50 rounded-lg font-medium hover:bg-zinc-100 dark:hover:bg-zinc-900 transition-colors"
          >
            Sign Up
          </Link>
        </div>
      </main>
    </div>
  );
}
