/** Input — single-line text field with an optional label and error. */
import { forwardRef } from 'react';
import { Text, TextInput, View, type TextInputProps } from 'react-native';
import { colors } from '@/lib/theme/tokens';

export type InputProps = TextInputProps & {
  label?: string;
  error?: string;
};

export const Input = forwardRef<TextInput, InputProps>(function Input(
  { label, error, className, ...rest },
  ref
) {
  return (
    <View className="gap-xs">
      {label ? <Text className="font-body-medium text-sm text-foreground">{label}</Text> : null}
      <TextInput
        ref={ref}
        placeholderTextColor={colors.light.mutedForeground}
        className={`rounded-lg border bg-card px-lg py-md font-body text-base text-foreground ${
          error ? 'border-destructive' : 'border-input'
        } ${className ?? ''}`}
        {...rest}
      />
      {error ? <Text className="font-body text-xs text-destructive">{error}</Text> : null}
    </View>
  );
});
