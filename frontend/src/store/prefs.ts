export interface WidgetPref {
  id: string;
  hidden: boolean;
}

const KEY = 'widget_prefs';

export function loadPrefs(): WidgetPref[] {
  const raw = localStorage.getItem(KEY);
  return raw ? JSON.parse(raw) : [];
}

export function savePrefs(prefs: WidgetPref[]) {
  localStorage.setItem(KEY, JSON.stringify(prefs));
}
