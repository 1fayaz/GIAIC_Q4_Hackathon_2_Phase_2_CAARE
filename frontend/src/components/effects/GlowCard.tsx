import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import GlowCardWrapper from './GlowCardWrapper';

interface GlowCardProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
  footer?: React.ReactNode;
  className?: string;
  glowIntensity?: number;
}

const GlowCard: React.FC<GlowCardProps> = ({
  children,
  title,
  description,
  footer,
  className = '',
  glowIntensity = 0.15
}) => {
  return (
    <GlowCardWrapper className={className} glowIntensity={glowIntensity}>
      <Card className="border-0 bg-transparent shadow-none">
        {title && (
          <CardHeader className="p-6 pb-4">
            {title && <CardTitle>{title}</CardTitle>}
            {description && <CardDescription>{description}</CardDescription>}
          </CardHeader>
        )}
        <CardContent className="p-6 pt-0">
          {children}
        </CardContent>
        {footer && (
          <CardFooter className="p-6 pt-0">
            {footer}
          </CardFooter>
        )}
      </Card>
    </GlowCardWrapper>
  );
};

export default GlowCard;