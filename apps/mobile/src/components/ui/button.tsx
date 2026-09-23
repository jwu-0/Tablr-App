/**
 * Button — the one pressable. Extend the variant/size maps rather than adding
 * one-off styles at call sites.
 */
import { forwardRef } from 'react';
import { ActivityIndicator, Pressable, Text, type PressableProps } from 'react-native';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'destructive';
export type ButtonSize = 'sm' | 'md' | 'lg';

const CONTAINER: Record<ButtonVariant, string> = {
  primary: 'bg-primary active:opacity-90',
  secondary: 'bg-secondary active:opacity-90',
  ghost: 'bg-transparent border border-border active:opacity-70',
  destructive: 'bg-destructive active:opacity-90',
};

const LABEL: Record<ButtonVariant, string> = {
  primary: 'text-primary-foreground',
  secondary: 'text-secondary-foreground',
  ghost: 'text-foreground',
  destructive: 'text-destructive-foreground',
};

const SIZE: Record<ButtonSize, string> = {
  sm: 'px-md py-sm',
  md: 'px-lg py-md',
  lg: 'px-xl py-lg',
};

const LABEL_SIZE: Record<ButtonSize, string> = {
  sm: 'text-sm',
  md: 'text-base',
  lg: 'text-lg',
};

export type ButtonProps = PressableProps & {
  title: string;
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
};

export const Button = forwardRef<React.ComponentRef<typeof Pressable>, ButtonProps>(function Button(
  { title, variant = 'primary', size = 'md', loading = false, disabled, className, ...rest },
  ref
) {
  return (
    <Pressable
      ref={ref}
      accessibilityRole="button"
      disabled={disabled || loading}
      className={`flex-row items-center justify-center rounded-lg ${CONTAINER[variant]} ${SIZE[size]} ${
        disabled || loading ? 'opacity-50' : ''
      } ${className ?? ''}`}
      {...rest}
    >
      {loading ? (
        <ActivityIndicator />
      ) : (
        <Text className={`font-body-medium ${LABEL[variant]} ${LABEL_SIZE[size]}`}>{title}</Text>
      )}
    </Pressable>
  );
});
