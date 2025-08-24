// utils/auth.ts
export async function checkAuth(): Promise<{
  is_authenticated: boolean;
  user?: string;
}> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/status/`, {
      method: "GET",
      credentials: "include", // important! sends session cookie
    });

    if (!res.ok) return { is_authenticated: false };

    return await res.json();
  } catch {
    return { is_authenticated: false };
  }
}

export async function logout() {
  await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logout/`, {
    method: "POST",
    credentials: "include",
  });
  window.location.href = "/";
}
