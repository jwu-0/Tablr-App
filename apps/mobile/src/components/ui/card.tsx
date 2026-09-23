/** Card — the standard raised surface (restaurant, table, profile). */
import type { PropsWithChildren } from 'react';
import { View, type ViewProps } from 'react-native';

export function Card({ children, className, ...rest }: PropsWithChildren<ViewProps>) {
  return (
    <View className={`rounded-xl border border-border bg-card p-lg ${className ?? ''}`} {...rest}>
      {children}
    </View>
  );
}
