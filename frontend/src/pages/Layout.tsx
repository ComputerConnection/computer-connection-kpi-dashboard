import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { useThemeStore } from '../store/theme';
import DateRangeControls from '../components/DateRangeControls';

export default function Layout() {
  const { dark, toggle } = useThemeStore();
  const location = useLocation();
  const links = [
    { to: '/sales', label: 'Sales' },
    { to: '/quotes', label: 'Quotes' },
    { to: '/repairs', label: 'Repairs' },
    { to: '/personal', label: 'Personal' },
  ];

  return (
    <div className={dark ? 'dark flex min-h-screen' : 'flex min-h-screen'}>
      <aside className="w-48 bg-gray-200 dark:bg-gray-800 p-4 space-y-2 hidden sm:block">
        {links.map((l) => (
          <Link
            key={l.to}
            className={
              'block px-2 py-1 rounded ' +
              (location.pathname === l.to ? 'bg-gray-300 dark:bg-gray-700' : '')
            }
            to={l.to}
            aria-current={location.pathname === l.to ? 'page' : undefined}
          >
            {l.label}
          </Link>
        ))}
        <button
          onClick={toggle}
          className="mt-4 text-sm text-blue-600 dark:text-blue-400"
          aria-label="Toggle dark mode"
        >
          Toggle Theme
        </button>
      </aside>
      <div className="flex-1">
        <header className="sm:hidden flex justify-between items-center p-2 bg-gray-200 dark:bg-gray-800">
          <span className="font-bold">KPI Dashboard</span>
          <button
            onClick={toggle}
            className="text-sm text-blue-600 dark:text-blue-400"
            aria-label="Toggle dark mode"
          >
            Toggle Theme
          </button>
        </header>
        <main className="p-4">
          <DateRangeControls />
          <Outlet />
        </main>
      </div>
    </div>
  );
}
