// context/AuthContext.tsx
"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { checkAuth, logout as apiLogout } from "../utils/auth";

type AuthContextType = {
  authenticated: boolean;
  username: string | null;
  refreshAuth: () => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType>({
  authenticated: false,
  username: null,
  refreshAuth: async () => {},
  logout: async () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setisAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | null>(null);

  const refreshAuth = async () => {
    const res = await checkAuth();
    setisAuthenticated(res.is_authenticated);
    setUsername(res.user ?? null);
  };

  const logout = async () => {
    await apiLogout();
    await refreshAuth();
  };

  useEffect(() => {
    refreshAuth();
  }, []);

  return (
    <AuthContext.Provider
      value={{ authenticated: isAuthenticated, username, refreshAuth, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
